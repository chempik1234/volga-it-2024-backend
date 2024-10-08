import json
import pika
from django.conf import settings
from threading import Event
from queue import Queue
# TODO: document microservice rabbit mq request timeout
auth_queue_request = settings.AUTH_QUEUE_REQUEST  # Used in outer calls, not linked to send/consume functions
auth_queue_response = settings.AUTH_QUEUE_RESPONSE
hospital_and_maybe_room_queue_request = settings.HOSPITAL_AND_MAYBE_ROOM_QUEUE_REQUEST
hospital_and_maybe_room_queue_response = settings.HOSPITAL_AND_MAYBE_ROOM_QUEUE_RESPONSE
role_queue_request = settings.ROLE_QUEUE_REQUEST
role_queue_response = settings.ROLE_QUEUE_RESPONSE

connection = None  # it will change during the first query/response, check the connect_to_rabbit_mq function


def connect_to_rabbit_mq():
    global connection
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))


def send_request_rabbit_mq(queue_name, message):
    """
    Basic function for sending rabbitMQ messages
    """
    if not connection:  # if connection hadn't been created, it's time to do it
        connect_to_rabbit_mq()
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    channel.basic_publish(exchange='', routing_key=queue_name, body=message)
    connection.close()


def consume_with_rabbit_mq(queue_name, function_check_data=None, ):
    """
    Basic function for receiving RabbitMQ messages from given queue
    """
    queue_for_callback_response = Queue()  # queue for the data storage
    response_event = Event()  # tells us that the data is ready to be returned

    def callback(ch, method, properties, body):
        print("DOCUMENT MICROSERVICE: RECEIVED MESSAGE", body, sep='\n')  # show message in terminal
        data = json.loads(body)  # get the data and return it!
        if function_check_data is None or function_check_data(data):
            return data
        queue_for_callback_response.put(data)
        response_event.set()

    if not connection:  # if connection hadn't been created, it's time to do it
        connect_to_rabbit_mq()
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

    response_event.wait()  # wait until we get the required data
    response = queue_for_callback_response.get()  # get it from the queue
    return response
