from catalog.services import BookService, AuthorService
from common.pb2 import book_pb2_grpc, author_pb2_grpc


def grpc_handlers(server):
    book_pb2_grpc.add_BookControllerServicer_to_server(BookService.as_servicer(), server)
    author_pb2_grpc.add_AuthorControllerServicer_to_server(AuthorService.as_servicer(), server)
