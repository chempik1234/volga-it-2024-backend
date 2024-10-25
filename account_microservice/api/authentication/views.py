import json
import logging

from django.contrib.auth import get_user_model, logout
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

from ..models import Role
from ..serializers import CustomUserSerializer, SignOutSerializer, CustomTokenObtainPairSerializer

logger = logging.getLogger(__name__)
User = get_user_model()


class SignUpView(GenericAPIView):
    """
    An endpoint for creating new users
    POST /api/Authentication/SignUp
    """
    allowed_methods = ["post",]
    http_method_names = ["post",]
    permission_classes = (AllowAny,)
    serializer_class = CustomUserSerializer
    queryset = User.objects.all()

    def post(self, request: Request) -> Response:
        # try:  # json body needs to be decoded, but if it contains syntax errors, an exception occures
        #     body_unicode = request.body.decode('utf-8')
        #     post_ = json.loads(body_unicode)
        # except json.JSONDecodeError:
        #     return Response({"error": "Invalid JSON format"}, status=status.HTTP_400_BAD_REQUEST)
        # except Exception as e:
        #     return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        post_ = request.data  # TODO: remove if deecoding works

        last_name, first_name, username, password = (post_.get("lastName"),
                                                     post_.get("firstName"),
                                                     post_.get('username'),
                                                     post_.get('password'))
        if not (last_name and first_name and username and password):  # these are required fields, ERROR 400 if absent
            return Response({"details": "lastName, firstName, username and password are required in body"},
                            status=status.HTTP_400_BAD_REQUEST)
        new_user = User()
        new_user.last_name = last_name
        new_user.first_name = first_name
        new_user.username = username
        new_user.set_password(password)
        new_user.save()
        new_user.roles.add(Role.objects.get_or_create(name="User"))
        return Response(self.serializer_class(new_user).data, status=status.HTTP_201_CREATED)


class SignInView(GenericAPIView):
    """
    An endpoint for signing users in via giving them their JWT pairs
    POST /api/Authentication/SignIn
    """
    allowed_methods = ["post"]
    http_method_names = ["post"]
    permission_classes = (AllowAny,)
    authentication_classes = []
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request: Request) -> Response:
        post_ = request.data

        username, password = post_.get('username'), post_.get('password')
        if not (username and password):  # these are required fields, ERROR 400 if absent
            return Response({"details": "username and password are required in body"},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data={"username": username, "password": password})
        if serializer.is_valid():  # A rest_framework serializer can automatically check the credentials
            return Response(serializer.validated_data, status=status.HTTP_200_OK)  # if it does, it returns 2 tokens
        else:  # if not - the user gets an errors list!
            return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class SignOutView(GenericAPIView):
    """
    An endpoint for signing users out via built-in django logout (REST API can't log them out itself, the client does)
    POST /api/Authentication/SignOut
    """
    allowed_methods = ["post"]
    http_method_names = ["post"]
    permission_classes = [IsAuthenticated,]
    serializer_class = SignOutSerializer

    def get_serializer_class(self):
        return self.serializer_class

    def post(self, request: Request) -> Response:

        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)
            logger.info(f"SIGNED OUT TOKEN {token} OF USER WITH ID {request.user.id}")
        # TODO: make this shit work

        return Response(self.serializer_class().data, status=status.HTTP_205_RESET_CONTENT)
