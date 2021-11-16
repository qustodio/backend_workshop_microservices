from django_grpc_framework import proto_serializers

from catalog.models import Book, Author
from common.pb2 import book_pb2, author_pb2


class BookProtoSerializer(proto_serializers.ModelProtoSerializer):
    class Meta:
        model = Book
        proto_class = book_pb2.Book
        fields = ['id', 'title', 'isbn', 'author', 'genre', 'summary', 'language']


class AuthorProtoSerializer(proto_serializers.ModelProtoSerializer):
    class Meta:
        model = Author
        proto_class = author_pb2.Author
        fields = ['id', 'first_name', 'last_name', 'date_of_birth', 'date_of_death']
