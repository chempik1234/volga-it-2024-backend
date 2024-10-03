import json

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Visit
from .rabbit_mq import send_request_rabbit_mq, hospital_and_maybe_room_queue_request, \
    consume_with_rabbit_mq, hospital_and_maybe_room_queue_response, role_queue_request, role_queue_response
from .services import RoleCheckService


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
        fields = ("date", "patientId", "doctorId", "hospitalId", "room", "data")

    def validate_hospitalId(self, value):
        """
        hospitalId "object exists" validator that uses sync RabbitMq request-response (senseless but cool!)
        """
        message = {"hospital_id": value}
        send_request_rabbit_mq(hospital_and_maybe_room_queue_request, json.dumps(message)) # 1) send validation request
        response = consume_with_rabbit_mq(  # 2) get response with hospital info
            hospital_and_maybe_room_queue_response, lambda x: (x.get('hospital_id', '') == value))
        if response.get('hospital', None):
            return value
        else:
            raise ValidationError("hospital id couldn't be validated!")

    def validate_doctorId(self, value):
        """
        doctorId "object exists" validator that uses sync RabbitMq request-response (senseless but cool!)

        - checks role Doctor
        """
        response = RoleCheckService().check_role(value, 'Doctor')
        if response.get('user', None):
            return value
        else:
            raise ValidationError("doctor id couldn't be validated!")

    def validate_patientId(self, value):
        """
        patientId "object exists" validator that uses sync RabbitMq request-response (senseless but cool!)

        - checks role User
        """
        response = RoleCheckService().check_role(value, 'User')
        if response.get('user', None):
            return value
        else:
            raise ValidationError("patient id couldn't be validated!")

    def validate(self, data):
        room_name, hospital_id = data.get("room"), data.get("hospitalId")
        message = {"room_name": room_name, "hospital_id": hospital_id}
        send_request_rabbit_mq(hospital_and_maybe_room_queue_request, json.dumps(message))  # 1) send validation request
        response = consume_with_rabbit_mq(  # 2) get response with room info
            hospital_and_maybe_room_queue_response, lambda x: (x.get('room_name', '') == room_name))
        if response.get('room', None) is None:
            raise ValidationError("Room with given name and hospital doesn't exist!")
        return data

