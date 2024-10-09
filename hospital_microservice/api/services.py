import logging

from django.contrib.auth import get_user_model
from django_grpc_framework import services

from .rpc_data_processors import data_process_hospital_or_room
from .proto.hospital_pb2 import *

logger = logging.getLogger(__name__)
User = get_user_model()


class HospitalGrpcService(services.Service):
    """
    gRPC service that allows to find Hospital & Room objects by hospital_id & maybe room_name
    """
    def ValidateHospital(self, request, context):
        """
        request: {"hospital_id": int}

        response: {"hospital_id": int, valid: bool}
        """
        result = data_process_hospital_or_room(request.hospital_id)
        return HospitalResponse(**result)

    def ValidateRoom(self, request, context):
        """
        request: {"hospital_id": int, "room_name": }

        response: {"hospital_id": int, valid: bool}
        """
        result = data_process_hospital_or_room(request.hospital_id, room_name=request.room_name)
        return RoomResponse(**result)


