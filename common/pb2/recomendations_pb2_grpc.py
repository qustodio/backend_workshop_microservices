# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from common.pb2 import recomendations_pb2 as recomendations__pb2

class RecomendationsControllerStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.List = channel.unary_stream(
                '/recomendator.RecomendationsController/List',
                request_serializer=recomendations__pb2.RecomendationsRequest.SerializeToString,
                response_deserializer=recomendations__pb2.Book.FromString,
                )


class RecomendationsControllerServicer(object):
    """Missing associated documentation comment in .proto file."""

    def List(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_RecomendationsControllerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'List': grpc.unary_stream_rpc_method_handler(
                    servicer.List,
                    request_deserializer=recomendations__pb2.RecomendationsRequest.FromString,
                    response_serializer=recomendations__pb2.Book.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'recomendator.RecomendationsController', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class RecomendationsController(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def List(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/recomendator.RecomendationsController/List',
            recomendations__pb2.RecomendationsRequest.SerializeToString,
            recomendations__pb2.Book.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
