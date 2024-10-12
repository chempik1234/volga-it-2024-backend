from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, inline_serializer
from rest_framework import status, serializers
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenRefreshView

from ..serializers import CustomTokenVerifySerializer


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(name='accessToken', description='Access Token as it is', type=str),
        ]
    )
)
class CustomTokenVerifyView(GenericAPIView):
    """
    An endpoint for token validation, simply returns: { valid: bool }
    GET /api/Authentication/Validate ?accessToken=
    """
    allowed_methods = ["get"]
    http_method_names = ["get"]
    serializer_class = CustomTokenVerifySerializer

    def get(self, request: Request) -> Response:
        access_token = request.query_params.get("accessToken")  # try to retrieve the token from params
        if not access_token:  # it's required, so ERROR 400 is thrown if absent
            return Response({'error': 'Access token is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            AccessToken(access_token)  # check the token with rest_framework
            return Response(self.serializer_class(data={"valid": True}).data, status=status.HTTP_200_OK)
        except TokenError:  # if it's invalid, an exception is raised, so ERROR 401 should be thrown in response
            return Response(self.serializer_class(data={"valid": False}).data, status=status.HTTP_401_UNAUTHORIZED)


@extend_schema_view(
    post=extend_schema(
        request=inline_serializer(
            name="JWTRefreshSerializer",
            fields={
                "refreshToken": serializers.CharField(allow_blank=False, allow_null=False)
            }
        )
    )
)
class CustomTokenRefreshView(TokenRefreshView):
    """
    SimpleJWT's "TokenRefreshView" but with the "refreshToken" key, not "refresh" as usual
    POST /api/Authentication/Refresh
    """
    def post(self, request: Request, *args, **kwargs) -> Response:
        refresh_token = request.data.get('refreshToken')  # get the token from request body
        if not refresh_token:  # it's required, so ERROR 400 is thrown if absent
            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)
        request._body = f"refresh={refresh_token}".encode()  # rename according to library standard
        request.data.update({"refresh": refresh_token})
        return super().post(request, args, kwargs)  # let rest_framework handle the token
