from .proto import account_pb2_grpc
from .services import UserGrpcService
from django.conf import settings

GRPC_PORT_ACCOUNT = settings.GRPC_PORT_ACCOUNT


def grpc_handlers(server):
    account_pb2_grpc.add_AccountRpcServiceServicer_to_server(UserGrpcService.as_servicer(), server)
    server.add_insecure_port(f"0.0.0.0:{GRPC_PORT_ACCOUNT}")
    server.start()
    server.wait_for_termination()
