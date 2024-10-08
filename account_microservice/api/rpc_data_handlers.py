# from __future__ import absolute_import

import logging

from django.contrib.auth import get_user_model
# from celery import shared_task

from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken
from .rabbit_mq import start_consuming_with_rabbit_mq, auth_queue_request, role_queue_request, \
    role_queue_response, auth_queue_response
from .serializers import CustomUserSerializerWithRoles

logger = logging.getLogger(__name__)
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
