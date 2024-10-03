import json

from .rabbit_mq import send_request_rabbit_mq, role_queue_request, consume_with_rabbit_mq, \
    role_queue_response


class RoleCheckService:
    """
    A simple service class that

    - checks if the User with user_id role via rabbit mq ROLE_QUEUE_REQUEST request
    - `returns the {"user_id": any, "role": any, "user": {...}}` response (the "user" key is used only if the response is successful
    """
    def __init__(self):
        pass

    def check_role(self, user_id, role):
        """
        Checks if the User with user_id role via rabbit mq ROLE_QUEUE_REQUEST request
        """
        message = {"user_id": user_id, 'role': role}
        send_request_rabbit_mq(role_queue_request, json.dumps(message))

        response = consume_with_rabbit_mq(role_queue_response, lambda x: x.get('user_id', '') == user_id)
        return response
