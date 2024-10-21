# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from . import hospital_pb2 as hospital__pb2

GRPC_GENERATED_VERSION = '1.66.2'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in hospital_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class HospitalRpcServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ValidateHospital = channel.unary_unary(
                '/HospitalRpcService/ValidateHospital',
                request_serializer=hospital__pb2.HospitalRequest.SerializeToString,
                response_deserializer=hospital__pb2.HospitalResponse.FromString,
                _registered_method=True)
        self.ValidateRoom = channel.unary_unary(
                '/HospitalRpcService/ValidateRoom',
                request_serializer=hospital__pb2.RoomRequest.SerializeToString,
                response_deserializer=hospital__pb2.RoomResponse.FromString,
                _registered_method=True)
        self.HospitalDeleted = channel.unary_unary(
                '/HospitalRpcService/HospitalDeleted',
                request_serializer=hospital__pb2.HospitalDeletedRequest.SerializeToString,
                response_deserializer=hospital__pb2.HospitalDeletedResponse.FromString,
                _registered_method=True)


class HospitalRpcServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ValidateHospital(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ValidateRoom(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def HospitalDeleted(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_HospitalRpcServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ValidateHospital': grpc.unary_unary_rpc_method_handler(
                    servicer.ValidateHospital,
                    request_deserializer=hospital__pb2.HospitalRequest.FromString,
                    response_serializer=hospital__pb2.HospitalResponse.SerializeToString,
            ),
            'ValidateRoom': grpc.unary_unary_rpc_method_handler(
                    servicer.ValidateRoom,
                    request_deserializer=hospital__pb2.RoomRequest.FromString,
                    response_serializer=hospital__pb2.RoomResponse.SerializeToString,
            ),
            'HospitalDeleted': grpc.unary_unary_rpc_method_handler(
                    servicer.HospitalDeleted,
                    request_deserializer=hospital__pb2.HospitalDeletedRequest.FromString,
                    response_serializer=hospital__pb2.HospitalDeletedResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'HospitalRpcService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('HospitalRpcService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class HospitalRpcService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ValidateHospital(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/HospitalRpcService/ValidateHospital',
            hospital__pb2.HospitalRequest.SerializeToString,
            hospital__pb2.HospitalResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ValidateRoom(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/HospitalRpcService/ValidateRoom',
            hospital__pb2.RoomRequest.SerializeToString,
            hospital__pb2.RoomResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def HospitalDeleted(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/HospitalRpcService/HospitalDeleted',
            hospital__pb2.HospitalDeletedRequest.SerializeToString,
            hospital__pb2.HospitalDeletedResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
