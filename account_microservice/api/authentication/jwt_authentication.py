from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenRefreshView


class CustomTokenVerifyView(APIView):
    """
    An endpoint for token validation, simply returns: { valid: bool }
    GET /api/Authentication/Validate
    """
    def get(self, request: Request) -> Response:
        access_token = request.query_params.get("accessToken")  # try to retrieve the token from params
        if not access_token:  # it's required, so ERROR 400 is thrown if absent
            return Response({'error': 'Access token is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            AccessToken(access_token)  # check the token with rest_framework
            return Response({"valid": True}, status=status.HTTP_200_OK)
        except TokenError:  # if it's invalid, an exception is raised, so ERROR 401 should be thrown in response
            return Response({'valid': False}, status=status.HTTP_401_UNAUTHORIZED)


class CustomTokenRefreshView(TokenRefreshView):
    """
    SimpleJWT's "TokenRefreshView" but with the "refreshToken" key, not "refresh" as usual
    POST /api/Authentication/Refresh
    """
    def post(self, request: Request, *args, **kwargs) -> Response:
        refresh_token = request.body.get('refreshToken')  # get the token from request body
        if not refresh_token:  # it's required, so ERROR 400 is thrown if absent
            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)
        request._body = f"refresh={refresh_token}".encode()  # rename according to library standard
        return super().post(request, args, kwargs)  # let rest_framework handle the token
