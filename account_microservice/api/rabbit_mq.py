import json
import pika
from django.conf import settings
from threading import Event
from queue import Queue

from django.contrib.auth import get_user_model
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken

from account_microservice.api.serializers import CustomUserSerializerWithRoles

auth_queue_request = settings.AUTH_QUEUE_REQUEST
auth_queue_response = settings.AUTH_QUEUE_RESPONSE

connection = None  # it will change during the first query/response, check the connect_to_rabbit_mq function

User = get_user_model()


def connect_to_rabbit_mq():
    global connection
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))


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


def start_consuming_with_rabbit_mq(queue_name, function_check_data=None):
    """
    Start consuming the token queue to validate JWT's when other microservices send requests
    """
    queue_for_callback_response = Queue()  # queue for the data storage
    response_event = Event()  # tells us that the data is ready to be returned

    def callback(ch, method, properties, body):
        print("AUTH MICROSERVICE: RECEIVED MESSAGE", body, sep='\n')  # show message in terminal
        data = json.loads(body)  # {accessToken: string}
        access_token = data.get('accessToken')
        try:
            user_id = AccessToken(access_token).get("id")  # check the token with rest_framework; if it's valid, get ID
            user_from_token = User.objects.get(user_id)
            message = {
                "accessToken": access_token,                         # genius message identification
                "user": CustomUserSerializerWithRoles(user_from_token).data}  # user data for other microservice
        except TokenError:
            message = {
                "accessToken": access_token  # genius message identification
            }                                # user data is None
        send_request_rabbit_mq(auth_queue_response, json.dumps(message))

    if not connection:  # if connection hadn't been created, it's time to do it
        connect_to_rabbit_mq()
    channel_request = connection.channel()
    channel_request.queue_declare(queue=queue_name)
    channel_request.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel_request.start_consuming()
