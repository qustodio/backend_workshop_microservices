import datetime

from django_grpc_framework import proto_serializers
from rest_framework import serializers

from recomendations.models import Book, Author, BookInstance
from common.pb2 import book_pb2, author_pb2, book_instance_pb2, recomendations_pb2


class BookProtoSerializer(proto_serializers.ModelProtoSerializer):
    class Meta:
        model = Book
        proto_class = book_pb2.Book
        fields = ['id', 'title', 'isbn', 'author', 'genre', 'summary', 'language']

class BookRecomendationProtoSerializer(proto_serializers.ModelProtoSerializer):
    class Meta:
        model = Book
        proto_class = recomendations_pb2.Book
        fields = ['id']


class AuthorProtoSerializer(proto_serializers.ModelProtoSerializer):
    class Meta:
        model = Author
        proto_class = author_pb2.Author
        fields = ['id', 'first_name', 'last_name', 'date_of_birth', 'date_of_death']


class BookInstanceProtoSerializer(proto_serializers.ModelProtoSerializer):
    class Meta:
        model = BookInstance
        proto_class = book_instance_pb2.BookInstance
        fields = ['id', 'book', 'imprint', 'due_back', 'borrower', 'status']

    id = serializers.UUIDField(read_only=True)
