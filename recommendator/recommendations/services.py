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

from recommendations.models import Book, UserRecommendation
from recommendations.serializers import BookRecommendationProtoSerializer

class RecommendationService(Service):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.grpc_catalog_channel = grpc.insecure_channel(
            f"{settings.CATALOG_GRPC_HOST}:{settings.CATALOG_GRPC_PORT}"
        )

    def List(self, request, context):
        user_id = request.id

        books = self.get_all_books()
        book_intances = self.get_book_instances_from_user(user_id=user_id)

        recommended_authors = []
        recommended_genres = []
        books_readed = []
        for book_instance in book_intances:
            recommended_authors.append(self.get_book(book_instance.book).author)
            recommended_genres += list(self.get_book(book_instance.book).genre)
            books_readed.append(book_instance.book)

        

        books = self.calculate_recommendations(
            books_readed=books_readed,
            recommended_authors=recommended_authors,
            recommended_genres=recommended_genres,
            all_books=books
        )
        book_instances = self.save_recommended_books(recommended_books=books)
        UserRecommendation.objects.create(
            user=user_id,
        ).books.set(book_instances)


        serializer = BookRecommendationProtoSerializer(books, many=True)
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

    def calculate_recommendations(
        self,
        books_readed,
        recommended_authors,
        recommended_genres,
        all_books,
        num_recommendations=2
    ):
        random_recommended_books = []
        recommended_books = []
        for book in all_books:
            if book.id in books_readed:
                continue

            if len(recommended_books) >= num_recommendations:
                break

            if len(random_recommended_books) < num_recommendations:
                random_recommended_books.append(book)

            if book.author in recommended_authors:
                recommended_books.append(book)
                continue
            
            for genre in list(book.genre):
                if genre in recommended_genres:
                    recommended_books.append(book)
                    continue

        return recommended_books if len(recommended_books) > 0 else random_recommended_books

    def save_recommended_books(self, recommended_books):
        return [
            Book.objects.get_or_create(pk=book.id)[0]
            for book in recommended_books
        ]

        