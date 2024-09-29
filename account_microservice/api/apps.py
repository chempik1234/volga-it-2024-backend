from django.apps import AppConfig
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken

from account_microservice.api.rabbit_mq import start_consuming_with_rabbit_mq, auth_queue_request, doctor_queue_request, \
    doctor_queue_response, auth_queue_response
from account_microservice.api.serializers import CustomUserSerializerWithRoles


User = get_user_model()


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        from . import signals  # signals in this project are made for performing auto-caching and cleaning cache

        def data_process_function_jwt_queue(data):
            """
            Function to process data from RabbitMQ request.
            Validates and returns the JWT, also returns the user data if it's valid
            """
            message = data
            if data.get('accessToken', None):
                access_token = data.get('accessToken')
                try:
                    user_id = AccessToken(access_token).get("id")  # get the id from the token with rest_framework
                    user_from_token = User.objects.get(user_id)
                    message = {
                        "accessToken": access_token,                         # genius message identification
                        "user": CustomUserSerializerWithRoles(user_from_token).data}  # user data for other microservice
                except TokenError:  # if the token is invalid, then we can't send the user data cause it's None
                    message = {
                        "accessToken": access_token  # genius message identification
                    }                                # user data is None
            return message, auth_queue_response

        def data_process_function_doctor_queue(data):
            """
            Function to process data from RabbitMQ request.
            Gets the doctorId and then returns is with serialized doctor data if it's valid
            """
            if data.get("doctor_id", None):  # if it's a doctorId validation queue, then we try to find it among Users
                doctor_with_given_id = User.objects.filter(id=int(data.get("doctor_id")), roles__name="Doctor")
                if doctor_with_given_id.exists():  # if the doctor exists, we must return his data
                    data["doctor"] = CustomUserSerializerWithRoles(doctor_with_given_id.first()).data
            return data, doctor_queue_response

        start_consuming_with_rabbit_mq(doctor_queue_request, data_process_function_doctor_queue)
        start_consuming_with_rabbit_mq(auth_queue_request, data_process_function_jwt_queue)
