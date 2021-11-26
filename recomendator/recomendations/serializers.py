import base64

from django_grpc_framework import proto_serializers
from rest_framework import serializers

from common.pb2 import book_pb2, recomendations_pb2
from recomendations.models import Book


class BinaryField(serializers.Field):
    def to_representation(self, value):
        value_bytes = base64.decodebytes(value)
        return value_bytes.decode()

    def to_internal_value(self, value):
        value_bytes = value.encode()
        return base64.encodebytes(value_bytes)


class BookProtoSerializer(proto_serializers.ModelProtoSerializer):
    summary = serializers.CharField(allow_null=True, allow_blank=True)
    image = BinaryField(allow_null=True)

    class Meta:
        model = Book
        proto_class = book_pb2.Book
        fields = ['id', 'title', 'isbn', 'author', 'genre', 'summary', 'language', 'image']


class BookRecomendationProtoSerializer(proto_serializers.ModelProtoSerializer):
    class Meta:
        model = Book
        proto_class = recomendations_pb2.Book
        fields = ['id']
