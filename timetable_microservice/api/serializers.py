import json
import logging
from datetime import datetime, timedelta

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Timetable, Appointment
from .grpc_consume_produce import grpc_check_room, grpc_check_hospital, grpc_check_roles


class TimetableSerializer(serializers.ModelSerializer):
    """
    Timetable Serializer with changed field names from -> timeFrom; to -> timeTo
    validates hospital and doctor foreign keys with RabbitMQ!
    """
    hospitalId = serializers.IntegerField(source="hospital_id")
    doctorId = serializers.IntegerField(source="doctor_id")
    timeFrom = serializers.DateTimeField(source="time_from")  # TODO: tell about this change in swagger documentation
    timeTo = serializers.DateTimeField(source="time_to")

    class Meta:
        model = Timetable
        fields = ("id", "hospitalId", 'doctorId', "timeFrom", "timeTo", "room")

    def validate_hospitalId(self, value):
        """
        hospitalId "object exists" validator that uses gRPC request-response
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
        if grpc_check_roles(user_id=value, role="Doctor"):
            return value

    def validate_timeFrom(self, value):
        if value.minute % 30 or value.second != 0:
            raise ValidationError("Minutes must be a multiple of 30, and seconds must be equal to 0 in timeFrom!")
        return value

    def validate_timeTo(self, value):
        if value.minute % 30 or value.second != 0:
            raise ValidationError("Minutes must be a multiple of 30, and seconds must be equal to 0 in timeTo!")
        return value

    def validate(self, data):
        room_name, hospital_id = data.get("room"), data.get("hospital_id")
        if not grpc_check_room(hospital_id=hospital_id, room_name=room_name):
            raise ValidationError("Room with given name and hospital doesn't exist!")

        time_from = data.get('time_from')
        time_to = data.get('time_to')

        if time_from >= time_to:
            raise ValidationError("timeFrom mustn't be later or equal to timeTo!")
        elif time_from < time_to - timedelta(hours=12):
            raise ValidationError("difference between timeFrom and timeTo mustn't be greater that 12h!")
        return data


class AppointmentSerializer(serializers.ModelSerializer):
    """
    Simple appointment model serializer.
    """
    timetable = serializers.PrimaryKeyRelatedField(queryset=Timetable.objects.all())

    class Meta:
        model = Appointment
        fields = ("id", "user_id", "timetable", "time")

    def validate(self, data):
        timetable = data.get("timetable")
        time = data.get("time")
        if Appointment.objects.filter(timetable=timetable, time=time).exists():
            raise ValidationError("Appointment on that timetable on the same time already exists!")
        if time < timetable.time_from or time > timetable.time_to:
            raise ValidationError(f"Appointment tiime {time} must have been between {timetable.time_from} and "
                                  f"{timetable.time_to}!")
        if (time - timetable.time_from).seconds % 1800:
            raise ValidationError(f"Invalid appointment time: difference from {timetable.time_from} must be a "
                                  f"multiple of 30, not {round((time - timetable.time_from).seconds / 60, 2)}!")
        return data
