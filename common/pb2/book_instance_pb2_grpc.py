# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from common.pb2 import book_instance_pb2 as catalog_dot_book__instance__pb2


class BookInstanceControllerStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.List = channel.unary_stream(
        '/catalog.BookInstanceController/List',
        request_serializer=catalog_dot_book__instance__pb2.BookInstanceListRequest.SerializeToString,
        response_deserializer=catalog_dot_book__instance__pb2.BookInstance.FromString,
        )
    self.Create = channel.unary_unary(
        '/catalog.BookInstanceController/Create',
        request_serializer=catalog_dot_book__instance__pb2.BookInstance.SerializeToString,
        response_deserializer=catalog_dot_book__instance__pb2.BookInstance.FromString,
        )
    self.MyList = channel.unary_stream(
        '/catalog.BookInstanceController/MyList',
        request_serializer=catalog_dot_book__instance__pb2.MyBookInstanceListRequest.SerializeToString,
        response_deserializer=catalog_dot_book__instance__pb2.BookInstance.FromString,
        )
    self.Renew = channel.unary_unary(
        '/catalog.BookInstanceController/Renew',
        request_serializer=catalog_dot_book__instance__pb2.BookInstanceRenewal.SerializeToString,
        response_deserializer=catalog_dot_book__instance__pb2.BookInstance.FromString,
        )


class BookInstanceControllerServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def List(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Create(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def MyList(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Renew(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_BookInstanceControllerServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'List': grpc.unary_stream_rpc_method_handler(
          servicer.List,
          request_deserializer=catalog_dot_book__instance__pb2.BookInstanceListRequest.FromString,
          response_serializer=catalog_dot_book__instance__pb2.BookInstance.SerializeToString,
      ),
      'Create': grpc.unary_unary_rpc_method_handler(
          servicer.Create,
          request_deserializer=catalog_dot_book__instance__pb2.BookInstance.FromString,
          response_serializer=catalog_dot_book__instance__pb2.BookInstance.SerializeToString,
      ),
      'MyList': grpc.unary_stream_rpc_method_handler(
          servicer.MyList,
          request_deserializer=catalog_dot_book__instance__pb2.MyBookInstanceListRequest.FromString,
          response_serializer=catalog_dot_book__instance__pb2.BookInstance.SerializeToString,
      ),
      'Renew': grpc.unary_unary_rpc_method_handler(
          servicer.Renew,
          request_deserializer=catalog_dot_book__instance__pb2.BookInstanceRenewal.FromString,
          response_serializer=catalog_dot_book__instance__pb2.BookInstance.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'catalog.BookInstanceController', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
