import logging
from typing import Optional

import grpc
from drf_spectacular.contrib.rest_framework_simplejwt import SimpleJWTScheme
from drf_spectacular.drainage import warn
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import Token

from .proto import account_pb2_grpc as pb2_grpc
from .proto.account_pb2 import *

logger = logging.getLogger(__name__)


class SimplifiedJWTAuthentication(JWTAuthentication):
    """
    JWT Authenticator that checks user via gRPC
    """

    def get_user(self, validated_token):  # TODO: MAKE THIS SHIT WORK
        logger.error("STARTING CHANNEL")
        # channel = grpc.insecure_channel(f"127.0.0.1:60051")
        # logger.error("STARTING CLIENT")
        # client = pb2_grpc.AccountRpcServiceStub(channel)
        # logger.error("STARTING REQUEST")
        # req = JWTRequest(jwt=validated_token)
        # logger.error("STARTING WAITING")
        # resp = client.ValidateJWT(req)
        # logger.error("RESPONSE: ", resp)
        # user = resp.get("user", None)
        user = None
        return user

    def authenticate(self, request):
        """
        validate user but don't try to find him
        """
        logger.info("TRYINA AUTHENTICATE")
        return super().authenticate(request)

    def get_validated_token(self, raw_token: bytes) -> Token:
        logger.info(f"TRYINA VALIDATE {raw_token}")
        return super().get_validated_token(raw_token)

    def get_raw_token(self, header: bytes) -> Optional[bytes]:
        logger.info(f"TRYING GET RAW TOKEN {header}")
        return super().get_raw_token(header)

    def get_header(self, request: Request) -> bytes:
        logger.info(f"TRYING GET HEADER {request}")
        return super().get_header(request)

    def authenticate_header(self, request: Request) -> str:
        logger.info(f"TRYING AUTHTE HEADER {request}")
        return super().authenticate_header(request)


class CustomSimpleJWTScheme(SimpleJWTScheme):
    target_class = 'api.authenticator.SimplifiedJWTAuthentication'
