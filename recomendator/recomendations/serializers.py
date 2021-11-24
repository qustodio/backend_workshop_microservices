import datetime

from django_grpc_framework import proto_serializers

from recomendations.models import Book
from common.pb2 import book_pb2, recomendations_pb2


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
