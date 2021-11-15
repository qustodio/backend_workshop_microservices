from catalog.services import BookService
from common.pb2 import book_pb2_grpc


def grpc_handlers(server):
    book_pb2_grpc.add_BookControllerServicer_to_server(BookService.as_servicer(), server)
