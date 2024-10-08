import logging

from django.contrib.auth import get_user_model
from django.db import transaction
from django_grpc_framework import services

from .serializers import CustomUserSerializerWithRoles
# from .proto import account_pb2_grpc as pb2_grpc

logger = logging.getLogger(__name__)
User = get_user_model()


class UserGrpcService(services.Service):
    """
    gRPC service that allows to find User objects by id & maybe role
    """
    def ValidateJWT(self, request, context):
        logger.info(f"DUUUDE!!! JWT!!! {request}")

    def ValidateUser(self, request, context):
        logger.info(f"DUUUDE!!! USERSSS!!! {request}")


