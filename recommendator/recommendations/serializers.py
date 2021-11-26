import base64

from django_grpc_framework import proto_serializers
from rest_framework import serializers

from recommendations.models import Book
from common.pb2 import book_pb2, recommendations_pb2


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


class BookRecommendationProtoSerializer(proto_serializers.ModelProtoSerializer):
    class Meta:
        model = Book
        proto_class = recommendations_pb2.Book
        fields = ['id']
