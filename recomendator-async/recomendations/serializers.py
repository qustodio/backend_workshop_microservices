from django_grpc_framework import proto_serializers

from rest_framework import serializers

from recomendations.models import Book, BookInstance
from common.pb2 import book_pb2

class BookProtoSerializer(proto_serializers.ModelProtoSerializer):
    summary = serializers.CharField(allow_blank=True)

    class Meta:
        model = Book
        proto_class = book_pb2.Book
        fields = ['id', 'title', 'isbn', 'summary', 'author', 'genre', 'language']


class BookRecomendationProtoSerializer(proto_serializers.ModelProtoSerializer):
    class Meta:
        model = Book
        proto_class = book_pb2.Book
        fields = ['id']


class BookInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookInstance
        fields = ['id', 'book', 'imprint', 'due_back', 'borrower', 'status']

    id = serializers.UUIDField(read_only=True, format='hex')