import multiprocessing

from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        print("API STARTED")
        from . import signals  # signals in this project are made for performing auto-caching and cleaning cache
        from rest_framework_simplejwt.exceptions import TokenError
        from rest_framework_simplejwt.tokens import AccessToken
        from .rabbit_mq import start_consuming_with_rabbit_mq, auth_queue_request, role_queue_request, \
            role_queue_response, auth_queue_response
        from .serializers import CustomUserSerializerWithRoles
        from django.contrib.auth import get_user_model

        User = get_user_model()

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

        def data_process_function_role_queue(data):
            """
            Function to process data from RabbitMQ request.
            Gets the user id and then returns is with serialized user data if he has the required 'role': str
            """
            if data.get("user_id", None):  # if it's a doctorId validation queue, then we try to find it among Users
                doctor_with_given_id = User.objects.filter(id=int(data.get("user_id")))
                if data.get('role', None):
                    doctor_with_given_id = doctor_with_given_id.filter(roles__name=data.get('role'))
                if doctor_with_given_id.exists():  # if the doctor exists, we must return his data
                    data["user"] = CustomUserSerializerWithRoles(doctor_with_given_id.first()).data
            return data, role_queue_response

        processes = [multiprocessing.Process(target=start_consuming_with_rabbit_mq,
                                             args=(role_queue_request, data_process_function_role_queue)),
                     multiprocessing.Process(target=start_consuming_with_rabbit_mq,
                                             args=(auth_queue_request, data_process_function_jwt_queue))]
        for i in processes:
            i.start()
            i.join()
