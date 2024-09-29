import json

from django.apps import AppConfig

from hospital_microservice.api.models import Hospital, Room
from hospital_microservice.api.rabbit_mq import start_consuming_with_rabbit_mq, hospital_and_maybe_room_queue_request, \
    doctor_queue_request, send_request_rabbit_mq, hospital_and_maybe_room_queue_response
from hospital_microservice.api.serializers import HospitalSerializer, RoomSerializer


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        from . import signals  # signals in this project are made for performing auto-caching and cleaning cache
        # and also CASCADE on delete, there're linked models in timetable_microservice!

        def data_process_function(data):
            """
            Function to process data from RabbitMQ request.

            It can validate either room or hospital.

            - if both "hospital_id" and "room_name" are sent, it returns them and serialized room if exists.
            - if only "hospital_id" is sent, it returns it with a serialized hospital if it exists, else only the id

            Uses RabbitMQ to get the doctor data and ORM to get the hospital data
            """
            hospital_id = data.get("hospital_id", None)
            if hospital_id is not None:
                hospital_id = int(hospital_id)
                room_name = data.get("room_name", None)
                if room_name is None:
                    hospital_with_given_id = Hospital.objects.filter(id=hospital_id)
                    if hospital_with_given_id.exists():
                        data["hospital"] = HospitalSerializer(hospital_with_given_id.first()).data
                else:
                    room_with_given_params = Room.objects.filter(name=room_name, hospital__id=hospital_id)
                    if room_with_given_params.exists():
                        data["room"] = RoomSerializer(room_with_given_params).data
            return data, hospital_and_maybe_room_queue_response

        start_consuming_with_rabbit_mq(hospital_and_maybe_room_queue_request, data_process_function)
