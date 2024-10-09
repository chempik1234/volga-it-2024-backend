import logging

from django.contrib.auth import get_user_model

from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.settings import api_settings
from .serializers import CustomUserSerializerWithRoles

logger = logging.getLogger(__name__)
User = get_user_model()


def data_process_function_jwt(token):
    """
    Function to process data from RPC request.
    Validates and returns the JWT, also returns the user data if it's valid

    Return format: {"jwt": token, "user": {... serialized ...}}
    """
    message = {"jwt": token}
    for AuthToken in api_settings.AUTH_TOKEN_CLASSES:
        try:
            user_id = AuthToken(token).get("id")  # get the id from the token with rest_framework
            user_from_token = User.objects.get(user_id)
            message = {
                "jwt": token,                         # genius message identification
                "user": CustomUserSerializerWithRoles(user_from_token).data}  # user data for other microservice
            return message
        except TokenError:  # if the token is invalid, then we can't send the user data cause it's None
            message = {
                "jwt": token  # genius message identification
            }                       # user data is None
    return message


def data_process_function_user_and_role(user_id, role=None):
    """
    Function to process data from RPC request.
    Gets the user id and then returns is with serialized user data if he has the required 'role': str

    Return format: {"user_id": user_id, "user": {... serialized ...}}
    """
    doctor_with_given_id = User.objects.filter(id=user_id)
    message = {"user_id": user_id}
    if role is not None:
        doctor_with_given_id = doctor_with_given_id.filter(roles__name=role)
        message['role'] = role
    if doctor_with_given_id.exists():  # if the doctor exists, we must return his data
        message["user"] = CustomUserSerializerWithRoles(doctor_with_given_id.first()).data
    return message


# @shared_task()
# def consume_roles():
#     logger.info("START CONSUMING ROLES (RabbitMQ)")
#     start_consuming_with_rabbit_mq(role_queue_request, data_process_function_role_queue)
#
#
# @shared_task()
# def consume_jwt():
#     logger.info("START CONSUMING JWT (RabbitMQ)")
#     start_consuming_with_rabbit_mq(auth_queue_request, data_process_function_jwt_queue)
#
#
# print("RABBITMQ STARTUP 0")
# consume_roles.delay()
# consume_jwt.delay()
