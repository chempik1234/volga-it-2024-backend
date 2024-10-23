import json

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .grpc_consume_produce import grpc_check_user_and_role, grpc_check_room, grpc_check_hospital
from .models import Visit


class VisitSerializer(serializers.ModelSerializer):
    """
    Visit model serializer
    validates hospital and doctor foreign keys with RabbitMQ!
    """
    patientId = serializers.IntegerField(source="patient_id")
    doctorId = serializers.IntegerField(source="doctor_id")
    hospitalId = serializers.IntegerField(source="hospital_id")

    class Meta:
        model = Visit
        fields = ('id', "date", "patientId", "doctorId", "hospitalId", "room", "data")

    def validate_hospitalId(self, value):
        """
        hospitalId "object exists" validator that uses sync gRPC request-response
        """
        if grpc_check_hospital(hospital_id=value):
            return value
        else:
            raise ValidationError("hospital id couldn't be validated!")

    def validate_doctorId(self, value):
        """
        doctorId "object exists" validator that uses sync gRPC request-response

        - checks role Doctor
        """
        _, is_valid = grpc_check_user_and_role(value, "Doctor")
        if is_valid:
            return value
        else:
            raise ValidationError("doctor id couldn't be validated!")

    def validate_patientId(self, value):
        """
        patientId "object exists" validator that uses sync gRPC request-response

        - checks role User
        """
        _, is_valid = grpc_check_user_and_role(value, "User")
        if is_valid:
            return value
        else:
            raise ValidationError("patient id couldn't be validated!")

    def validate(self, data):
        room_name, hospital_id = data.get("room"), data.get("hospital_id")

        room_is_valid = grpc_check_room(hospital_id, room_name)
        if not room_is_valid:
            raise ValidationError("Room with given name and hospital doesn't exist!")
        return data

