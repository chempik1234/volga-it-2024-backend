from .proto import account_pb2_grpc
from .services import UserGrpcService


def grpc_handlers(server):
    account_pb2_grpc.add_AccountRpcServiceServicer_to_server(UserGrpcService.as_servicer(), server)
