from django.conf import settings

from .proto import account_pb2_grpc
from .services import HospitalGrpcService

GRPC_PORT_HOSPITAL = settings.GRPC_PORT_HOSPITAL


def grpc_handlers(server):
    account_pb2_grpc.add_AccountRpcServiceServicer_to_server(HospitalGrpcService.as_servicer(), server)
    server.add_insecure_port(f"0.0.0.0:{GRPC_PORT_HOSPITAL}")
    server.start()
    server.wait_for_termination()
