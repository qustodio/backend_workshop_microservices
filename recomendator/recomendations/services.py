import grpc
import logging

from django.conf import settings
from django_grpc_framework.services import Service

from common.pb2 import (
    book_pb2_grpc,
    book_pb2,
    book_instance_pb2_grpc,
    book_instance_pb2
)

from recomendations.models import Book
from recomendations.serializers import BookRecomendationProtoSerializer

class RecomendationService(Service):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.grpc_catalog_channel = grpc.insecure_channel(
            f"{settings.CATALOG_GRPC_HOST}:{settings.CATALOG_GRPC_PORT}"
        )

    def List(self, request, context):
        user_id = request.id

        books = self.get_all_books()
        book_intances = self.get_book_instances_from_user(user_id=user_id)

        recomended_authors = []
        recomended_genres = []
        books_readed = []
        for book_instance in book_intances:
            recomended_authors.append(self.get_book(book_instance.book).author)
            recomended_genres += list(self.get_book(book_instance.book).genre)
            books_readed.append(book_instance.book)

        

        books = self.calculate_recomendations(
            books_readed=books_readed,
            recomended_authors=recomended_authors,
            recomended_genres=recomended_genres,
            all_books=books
        )
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

    def get_book(self, book_id):
        book_stub = book_pb2_grpc.BookControllerStub(self.grpc_catalog_channel)
        try:
            book = book_stub.Retrieve(book_pb2.BookRetrieveRequest(
                id=book_id
            ))
        except grpc.RpcError as rpc_error:
            logging.error(rpc_error.details())
            raise rpc_error
        
        return book

    def get_book_instances_from_user(self, user_id):
        book_instance_stub = book_instance_pb2_grpc.BookInstanceControllerStub(
            self.grpc_catalog_channel
        )
        try:
            response = book_instance_stub.MyList(
                book_instance_pb2.MyBookInstanceListRequest(
                    borrower=user_id
                )
            )
        except grpc.RpcError as rpc_error:
            logging.error(rpc_error.details())
            raise rpc_error
        
        return response

    def calculate_recomendations(
        self,
        books_readed,
        recomended_authors,
        recomended_genres,
        all_books,
        num_recomendations=2
    ):
        random_recomended_books = []
        recomended_books = []
        for book in all_books:
            if book.id in books_readed:
                continue

            if len(recomended_books) >= num_recomendations:
                break

            if len(random_recomended_books) < num_recomendations:
                random_recomended_books.append(book)

            if book.author in recomended_authors:
                recomended_books.append(book)
                continue
            
            for genre in list(book.genre):
                if genre in recomended_genres:
                    recomended_books.append(book)
                    continue

        return recomended_books if len(recomended_books) > 0 else random_recomended_books
