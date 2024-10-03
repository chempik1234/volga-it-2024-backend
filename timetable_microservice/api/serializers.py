import json
from datetime import datetime, timedelta

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Timetable, Appointment
from .rabbit_mq import send_request_rabbit_mq, hospital_and_maybe_room_queue_request, \
    consume_with_rabbit_mq, hospital_and_maybe_room_queue_response, role_queue_request, role_queue_response


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
        hospitalId "object exists" validator that uses sync RabbitMq request-response (senseless but cool!)
        """
        message = {"hospital_id": value}
        send_request_rabbit_mq(hospital_and_maybe_room_queue_request, json.dumps(message))  # 1) send validation request
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
        message = {"user_id": value, 'role': 'Doctor'}
        send_request_rabbit_mq(role_queue_request, json.dumps(message))  # 1) send validation request
        response = consume_with_rabbit_mq(  # 2) get response with hospital info
            role_queue_response, lambda x: (x.get('user_id', '') == value))
        if response.get('user', None):
            return value

    # def validate_room(self, value):  # TODO: delete if everything works
    #     """
    #     room "object exists" validator that uses sync RabbitMq request-response (senseless but cool!)
    #
    #     Tries to find a room only by name at this point. Name & hospital query is done afterward in validate()
    #     """
    #     message = {"room_name": value}
    #     send_request_rabbit_mq(hospital_and_maybe_room_queue_request, json.dumps(message))  # 1) send validation request
    #     response = consume_with_rabbit_mq(  # 2) get response with room info
    #         hospital_and_maybe_room_queue_response, lambda x: (x.get('room_name', '') == value))
    #     if response.get('room', None):
    #         return value

    def validate_timeFrom(self, value):
        time_from_validated_value = datetime.fromisoformat(value)
        if time_from_validated_value.minute % 30 or time_from_validated_value.second != 0:
            raise ValidationError("Minutes must be a multiple of 30, and seconds must be equal to 0 in timeFrom!")
        return value

    def validate_timeTo(self, value):
        time_to_validated_value = datetime.fromisoformat(value)
        if time_to_validated_value.minute % 30 or time_to_validated_value.second != 0:
            raise ValidationError("Minutes must be a multiple of 30, and seconds must be equal to 0 in timeTo!")
        return value

    def validate(self, data):
        room_name, hospital_id = data.get("room"), data.get("hospitalId")
        message = {"room_name": room_name, "hospital_id": hospital_id}
        send_request_rabbit_mq(hospital_and_maybe_room_queue_request, json.dumps(message))  # 1) send validation request
        response = consume_with_rabbit_mq(  # 2) get response with room info
            hospital_and_maybe_room_queue_response, lambda x: (x.get('room_name', '') == room_name))
        if response.get('room', None) is None:
            raise ValidationError("Room with given name and hospital doesn't exist!")

        time_from = datetime.fromisoformat(data.get('time_from'))
        time_to = datetime.fromisoformat(data.get('time_to'))

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
        if Appointment.objects.filter(timetable=timetable, time=datetime.fromisoformat(time)).exists():
            raise ValidationError("Appointment on that timetable on the same time already exists!")
        return data
