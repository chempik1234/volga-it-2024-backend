import logging

from django.contrib.auth import get_user_model
from django_grpc_framework import services

from .rpc_data_processors import data_process_function_jwt, data_process_function_user_and_role
from .proto.account_pb2 import *

logger = logging.getLogger(__name__)
User = get_user_model()


class UserGrpcService(services.Service):
    """
    gRPC service that allows to find User objects by id & maybe role
    """
    def ValidateJWT(self, request, context):
        """
        request: {"jwt": "..."}

        response: {"jwt": "...", "user": optional}
        """
        result = data_process_function_jwt(request.jwt)
        return JWTResponse(**result)

    def ValidateUser(self, request, context):
        """
        request: {"user_id": int, "role": optional}

        returns: {"user_id": int, "role": optional, "user": optional}
        """
        role = getattr(request, "role", None)
        result = data_process_function_user_and_role(request.user_id, role)
        return UserResponse(**result)


