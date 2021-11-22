import datetime
import logging

from django_grpc_framework import proto_serializers
from rest_framework import serializers

from catalog.models import Book, Author, BookInstance
from common.pb2 import book_pb2, author_pb2, book_instance_pb2


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

    def message_to_data(self, message):
        logging.warning(message)
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
