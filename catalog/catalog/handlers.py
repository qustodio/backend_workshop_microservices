from catalog.services import BookService, AuthorService, BookInstanceService, LanguageService
from common.pb2 import book_pb2_grpc, author_pb2_grpc, book_instance_pb2_grpc, language_pb2_grpc


def grpc_handlers(server):
    book_pb2_grpc.add_BookControllerServicer_to_server(BookService.as_servicer(), server)
    author_pb2_grpc.add_AuthorControllerServicer_to_server(AuthorService.as_servicer(), server)
    book_instance_pb2_grpc.add_BookInstanceControllerServicer_to_server(BookInstanceService.as_servicer(), server)
    language_pb2_grpc.add_LanguageControllerServicer_to_server(LanguageService.as_servicer(), server)

    # TODO register the handler servicer

