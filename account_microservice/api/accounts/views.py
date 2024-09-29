import json

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from account_microservice.api.permissions import IsAdminUserWithRole
from account_microservice.api.serializers import CustomUserSerializer, CustomUserSerializerWithRoles

User = get_user_model()


class MeView(APIView):
    """
    Current account details endpoint
    GET /api/Accounts/Me
    """
    permission_classes = [IsAuthenticated,]
    http_method_names = ['GET']
    allowed_methods = ["GET"]

    def get(self, request):
        return Response(CustomUserSerializer(request.user).data, status=status.HTTP_200_OK)


class UpdateAccountView(APIView):
    """
    Current account update endpoint
    PUT /api/Accounts/Update
    """
    permission_classes = [IsAuthenticated,]
    http_method_names = ['PUT']
    allowed_methods = ["PUT"]

    def put(self, request):
        put_ = request.data  # no need to decode the data

        last_name, first_name, password = put_.get("lastName"), put_.get("firstName"), put_.get("password")
        if not (last_name and first_name and password):  # these fields are retuired, so ERROR 400 is something's absent
            return Response({"details": "lastName, firstName and password are required!"},
                            status=status.HTTP_400_BAD_REQUEST)

        data = {"lastName": last_name, "firstName": first_name, "password": password}  # new user data

        serializer = CustomUserSerializer(request.user, data=data, partial=True)  # partial update
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:  # if data is invalid, then it's client's fault
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminAccountsViewSet(ModelViewSet):
    """
    ViewSet for admin accounts CRUD with roles creation support
    """
    queryset = User.objects.all()
    serializer_class = CustomUserSerializerWithRoles
    permission_classes = [IsAdminUserWithRole,]

    @action(detail=False, methods=['get'])
    def accounts(self, request):
        """
        Accounts list endpoint (from and count are query params, they limit the performed selection)
        GET /api/Accounts ?from &count
        """
        from_ = int(request.query_params.get('from', 0))
        count = int(request.query_params.get('count', 10))
        accounts = User.objects.all()[from_:from_ + count]
        serializer = CustomUserSerializer(accounts, many=True)
        return Response(serializer.data)

    # TODO: clear commented code if everything works
    # def create(self, request, args, kwargs):
    #     """
    #     The endpoint for creating User with roles (special body format requires the orverriding of create() method)
    #     POST /api/Accounts
    #     """
    #     try:  # json body needs to be decoded, but if it contains syntax errors, an exception occures
    #         body_unicode = request.body.decode('utf-8')
    #         post_ = json.loads(body_unicode)
    #     except json.JSONDecodeError:
    #         return Response({"error": "Invalid JSON format"}, status=status.HTTP_400_BAD_REQUEST)
    #     except Exception as e:
    #         return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    #
    #     serializer = self.get_serializer(data=post_)
    #     serializer.is_valid(raise_exception=True)
    #
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    #
    # def update(self, request, args, kwargs):
    #     """
    #     The endpoint for updating User with roles (special body format requires the orverriding of update() method)
    #     PUT /api/Accounts/{id}
    #     """
    #     put_ = request.data
    #
    #     serializer = self.get_serializer(data=put_)
    #     serializer.is_valid(raise_exception=True)
    #
    #     self.perform_update(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
