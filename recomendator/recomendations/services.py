import grpc
import logging

from django.conf import settings
from django_grpc_framework.services import Service

from common.pb2 import book_pb2_grpc, book_pb2

from recomendations.models import Book
from recomendations.serializers import BookRecomendationProtoSerializer

class RecomendationService(Service):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.grpc_catalog_channel = grpc.insecure_channel(
            f"{settings.CATALOG_GRPC_HOST}:{settings.CATALOG_GRPC_PORT}"
        )

    def List(self, request, context):
        """
        -[x] (1)
            1. Get all books
            2 Return all books
        - [ ] (2)
            1. Get user pk
            2. Get user book Instances
            3. Get other author books 
        - [ ] (3)
            1. Use 2
            2. Get other books genre
            3. return related books

        """
        books = self.get_all_books()
        serializer = BookRecomendationProtoSerializer(books, many=True)
        for msg in serializer.message:
            yield msg

    def get_all_books(self):
        book_stub = book_pb2_grpc.BookControllerStub(self.grpc_catalog_channel)
        try:
            response = book_stub.List(book_pb2.BookListRequest())
        except grpc.RpcError as rpc_error:
            logging.error(rpc_error.details())
            raise rpc_error
        
        return response
