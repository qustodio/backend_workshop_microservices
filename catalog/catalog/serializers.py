import datetime

from django_grpc_framework import proto_serializers
from django_grpc_framework.protobuf.json_format import (
    message_to_dict
)
from rest_framework import serializers

from catalog.models import Book, Author, BookInstance, Language, Genre
from common.pb2 import book_pb2, author_pb2, book_instance_pb2, language_pb2, genre_pb2


class BookProtoSerializer(proto_serializers.ModelProtoSerializer):
    summary = serializers.CharField(allow_blank=True)

    class Meta:
        model = Book
        proto_class = book_pb2.Book
        fields = ['id', 'title', 'isbn', 'summary', 'author', 'genre', 'language']


class AuthorProtoSerializer(proto_serializers.ModelProtoSerializer):
    class Meta:
        model = Author
        proto_class = author_pb2.Author
        fields = ['id', 'first_name', 'last_name', 'date_of_birth', 'date_of_death']

    def message_to_data(self, message):
        data = {
            'first_name': message.first_name,
            'last_name': message.last_name,
            'date_of_birth': message.date_of_birth,
        }

        if message.id and not message.date_of_death:
            data['date_of_death'] = None
        elif message.date_of_death:
            data['date_of_death'] = message.date_of_death

        return data


class BookInstanceProtoSerializer(proto_serializers.ModelProtoSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = BookInstance
        proto_class = book_instance_pb2.BookInstance
        fields = ['id', 'book', 'imprint', 'due_back', 'borrower', 'status']

    def message_to_data(self, message):
        data = message_to_dict(message)
        if message.due_back:
            data['due_back'] = message.due_back
        else:
            data['due_back'] = None
        if message.borrower:
            data['borrower'] = message.borrower
        else:
            data['borrower'] = None
        return data


class BookInstanceRenewalProtoSerializer(proto_serializers.ModelProtoSerializer):
    class Meta:
        model = BookInstance
        proto_class = book_instance_pb2.BookInstance
        fields = ['id', 'due_back', 'imprint', 'book', 'borrower', 'status']

    imprint = serializers.CharField(read_only=True)
    book = serializers.IntegerField(read_only=True, source='book.id')
    borrower = serializers.IntegerField(read_only=True, source='borrower.id')
    status = serializers.CharField(read_only=True)

    def validate(self, data):
        new_due_back = data['due_back']

        # Check date is not in past.
        if new_due_back < datetime.date.today():
            raise proto_serializers.ValidationError('Invalid date - renewal date in the past')

        # Check date is in range librarian allowed to change (+4 weeks)
        if new_due_back > datetime.date.today() + datetime.timedelta(weeks=4):
            raise proto_serializers.ValidationError('Invalid date - renewal more than 4 weeks ahead')

        return data


class LanguageProtoSerializer(proto_serializers.ModelProtoSerializer):
    class Meta:
        model = Language
        proto_class = language_pb2.Language
        fields = ['id', 'name']


class GenreProtoSerializer(proto_serializers.ModelProtoSerializer):
    class Meta:
        model = Genre
        proto_class = genre_pb2.Genre
        fields = ['id', 'name']
