import json
import logging

import pika
from django.conf import settings
from threading import Event
from queue import Queue

from django.contrib.auth import get_user_model
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken

from .serializers import CustomUserSerializerWithRoles

auth_queue_request = settings.AUTH_QUEUE_REQUEST  # Used in outer calls, not linked to send/consume functions
auth_queue_response = settings.AUTH_QUEUE_RESPONSE
hospital_and_maybe_room_queue_request = settings.HOSPITAL_AND_MAYBE_ROOM_QUEUE_REQUEST
hospital_and_maybe_room_queue_response = settings.HOSPITAL_AND_MAYBE_ROOM_QUEUE_RESPONSE
role_queue_request = settings.ROLE_QUEUE_REQUEST
role_queue_response = settings.ROLE_QUEUE_RESPONSE

connection = None  # it will change during the first query/response, check the connect_to_rabbit_mq function

User = get_user_model()

logger = logging.getLogger(__name__)


def connect_to_rabbit_mq():
    global connection
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))


def send_request_rabbit_mq(queue_name, message):
    """
    Basic function for sending rabbitMQ messages
    """
    if not connection:  # if connection hadn't been created, it's time to do it
        connect_to_rabbit_mq()
    channel_response = connection.channel()
    channel_response.queue_declare(queue=queue_name)
    channel_response.basic_publish(exchange='', routing_key=queue_name, body=message)
    connection.close()


def start_consuming_with_rabbit_mq(queue_name, data_process_function):
    """
    Basic function to consume RabbitMQ requests and give response.

    Uses the data_process_function to get response message from data.
    """

    def callback(ch, method, properties, body):
        logger.info(f"AUTH MICROSERVICE: RECEIVED MESSAGE {body}")  # show message in terminal
        data = json.loads(body)
        message, response_queue = data_process_function(data)
        send_request_rabbit_mq(response_queue, json.dumps(message))

    if not connection:  # if connection hadn't been created, it's time to do it
        connect_to_rabbit_mq()
    channel_request = connection.channel()
    channel_request.queue_declare(queue=queue_name)
    channel_request.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel_request.start_consuming()
