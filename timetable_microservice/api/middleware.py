import json

from django.utils.deprecation import MiddlewareMixin

from .rabbit_mq import send_request_rabbit_mq, consume_with_rabbit_mq, auth_queue_request, \
    auth_queue_response


class AuthenticationProxyingMiddleware(MiddlewareMixin):
    """
    Standard proxy auth middleware for our microservices.
    Uses the auth microservice via RabbitMQ to authenticate users is this exact microservice.
    """

    def process_request(self, request):
        auth_header = request.headers.get("HTTP_AUTHORIZATION")
        if auth_header:  # Bearer token_only
            token = auth_header.split()[1]  # token_only
            message = {"accessToken": token}

            send_request_rabbit_mq(auth_queue_request, json.dumps(message))  # 1) send validation request
            response = consume_with_rabbit_mq(                               # 2) get response with user info
                auth_queue_response, lambda x: (x.get('accessToken', '') == token))

            user_dict = response.get("user")  # CustomUserSerializerWithRoles.data
            if user_dict:
                request.user = user_dict  # we only need to know that user's not None => that's enough
