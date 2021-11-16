import grpc
from django_grpc_framework.services import Service
from google.protobuf import empty_pb2

from catalog.models import Book, Author
from catalog.serializers import BookProtoSerializer, AuthorProtoSerializer


class BookService(Service):
    def Create(self, request, context):
        serializer = BookProtoSerializer(message=request)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.message

    def get_object(self, pk):
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            self.context.abort(grpc.StatusCode.NOT_FOUND, 'Book:%s not found!' % pk)

    def Update(self, request, context):
        book = self.get_object(request.id)
        serializer = BookProtoSerializer(book, message=request)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.message

    def Destroy(self, request, context):
        book = self.get_object(request.id)
        book.delete()
        return empty_pb2.Empty()

    def Retrieve(self, request, context):
        book = self.get_object(request.id)
        serializer = BookProtoSerializer(book)
        return serializer.message

    def List(self, request, context):
        books = Book.objects.all()
        serializer = BookProtoSerializer(books, many=True)
        for msg in serializer.message:
            yield msg


class AuthorService(Service):
    def Create(self, request, context):
        serializer = AuthorProtoSerializer(message=request)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.message

    def get_object(self, pk):
        try:
            return Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            self.context.abort(grpc.StatusCode.NOT_FOUND, 'Book:%s not found!' % pk)

    def Update(self, request, context):
        author = self.get_object(request.id)
        serializer = AuthorProtoSerializer(author, message=request)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.message

    def Destroy(self, request, context):
        author = self.get_object(request.id)
        author.delete()
        return empty_pb2.Empty()

    def Retrieve(self, request, context):
        author = self.get_object(request.id)
        serializer = AuthorProtoSerializer(author)
        return serializer.message

    def List(self, request, context):
        authors = Author.objects.all()
        serializer = AuthorProtoSerializer(authors, many=True)
        for msg in serializer.message:
            yield msg
