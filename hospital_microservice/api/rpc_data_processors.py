import logging

from .models import Hospital, Room
from .serializers import HospitalSerializer, RoomSerializer

logger = logging.getLogger(__name__)


def data_process_hospital_or_room(hospital_id, room_name=None):
    """
    Function to process data from RPC request.

    It can validate either room or hospital.

    - if both "hospital_id" and "room_name" are sent, it returns them and serialized room if exists.
    - if only "hospital_id" is sent, it returns it with a serialized hospital if it exists, else only the id

    Uses gRPC to get the doctor data and ORM to get the hospital data
    """
    message = {"hospital_id": hospital_id, "valid": False}
    if room_name is None:
        hospital_with_given_id = Hospital.objects.filter(id=hospital_id)
        if hospital_with_given_id.exists():
            message["valid"] = True  # HospitalSerializer(hospital_with_given_id.first()).data
    else:
        room_with_given_params = Room.objects.filter(name=room_name, hospital__id=hospital_id)
        if room_with_given_params.exists():
            message["valid"] = True  # RoomSerializer(room_with_given_params).data
    return message
