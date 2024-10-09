import logging
import os
from typing import Optional, Tuple

from django.contrib.auth import get_user_model
from drf_spectacular.contrib.rest_framework_simplejwt import SimpleJWTScheme
from drf_spectacular.drainage import warn
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import Token, AccessToken

from .grpc_consume_produce import grpc_user_by_jwt

logger = logging.getLogger(__name__)

User = get_user_model()


class SimplifiedJWTAuthentication(JWTAuthentication):
    """
    JWT Authenticator that checks user via gRPC
    """

    def authenticate(self, request: Request) -> Optional[Tuple[dict, Token]]:
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

        return self.get_user(raw_token), validated_token

    def get_user(self, raw_token):
        return grpc_user_by_jwt(raw_token)

    def get_validated_token(self, raw_token: bytes) -> Token:
        """
        Validates an encoded JSON web token and returns a validated token
        wrapper object.
        """
        messages = []
        for AuthToken in api_settings.AUTH_TOKEN_CLASSES:
            try:
                return AuthToken(raw_token, verify=False)
            except TokenError as e:
                messages.append(
                    {
                        "token_class": AuthToken.__name__,
                        "token_type": AuthToken.token_type,
                        "message": e.args[0],
                    }
                )
#
        raise InvalidToken(
            {
                "detail": "Given token not valid for any token type",
                "messages": messages,
            }
        )


class CustomSimpleJWTScheme(SimpleJWTScheme):
    target_class = 'api.authenticator.SimplifiedJWTAuthentication'


class SimpleGPRCToken(AccessToken):
    pass
