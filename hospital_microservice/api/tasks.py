from __future__ import absolute_import

import logging

from celery import shared_task

from .models import Hospital, Room
from .rabbit_mq import start_consuming_with_rabbit_mq, hospital_and_maybe_room_queue_request, \
    role_queue_request, send_request_rabbit_mq, hospital_and_maybe_room_queue_response
from .serializers import HospitalSerializer, RoomSerializer

logger = logging.getLogger(__name__)


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


@shared_task()
def consume_hospitals_and_rooms():
    logger.info("STARTED CONSUMING HOSPITAL & ROOM QUEUE")
    start_consuming_with_rabbit_mq(hospital_and_maybe_room_queue_request, data_process_function)
