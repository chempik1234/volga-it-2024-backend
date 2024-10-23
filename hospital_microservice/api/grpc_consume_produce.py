import logging

import grpc

from .proto import account_pb2_grpc
from .proto.account_pb2 import *
from django.conf import settings

GRPC_PORT_ACCOUNT = settings.GRPC_PORT_ACCOUNT
logger = logging.getLogger(__name__)


def grpc_user_by_jwt(raw_token):
    try:
        channel = grpc.insecure_channel(f"account_microservice:{GRPC_PORT_ACCOUNT}")
        client = account_pb2_grpc.AccountRpcServiceStub(channel)
        request = JWTRequest(jwt=raw_token)
        response = client.ValidateJWT(request)
        user = getattr(response, "user", None)
        return user
    except Exception as e:
        logger.error(f"gRPC ERROR WHEN TRYINA CHECK JWT: {e}")
        return


def grpc_check_roles(user_id, role=None):
    try:
        channel = grpc.insecure_channel(f"account_microservice:{GRPC_PORT_ACCOUNT}")
        client = account_pb2_grpc.AccountRpcServiceStub(channel)
        request = UserRequest(user_id=user_id, role=role)
        response = client.ValidateUser(request)
        user = getattr(response, "user", None)
        return user, response.valid
    except Exception as e:
        logger.error(f"gRPC ERROR WHEN TRYINA CHECK USER (user_id = {user_id}) (role = {role}): {e}")
        return
