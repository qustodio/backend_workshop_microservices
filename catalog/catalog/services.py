import grpc
from django_grpc_framework.services import Service
from google.protobuf import empty_pb2

from catalog.models import Book, Author, BookInstance, Language, Genre
from catalog.serializers import BookProtoSerializer, AuthorProtoSerializer, BookInstanceProtoSerializer, \
    BookInstanceRenewalProtoSerializer, LanguageProtoSerializer


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
            self.context.abort(grpc.StatusCode.NOT_FOUND, 'Author:%s not found!' % pk)

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


class BookInstanceService(Service):
    def Create(self, request, context):
        serializer = BookInstanceProtoSerializer(message=request)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.message

    def Renew(self, request, context):
        book_instance = self.get_object(request.id)
        serializer = BookInstanceRenewalProtoSerializer(book_instance, message=request)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.message

    def MyList(self, request, context):
        book_instance_list = self.get_queryset(request.borrower)
        serializer = BookInstanceProtoSerializer(book_instance_list, many=True)
        for msg in serializer.message:
            yield msg

    def List(self, request, context):
        book_instance_list = self.get_queryset()
        serializer = BookInstanceProtoSerializer(book_instance_list, many=True)
        for msg in serializer.message:
            yield msg

    def get_object(self, pk):
        try:
            return BookInstance.objects.get(pk=pk, status__exact='o')
        except BookInstance.DoesNotExist:
            self.context.abort(grpc.StatusCode.NOT_FOUND, 'BookInstance:%s not found!' % id)

    def get_queryset(self, borrower=None):
        if borrower:
            return BookInstance.objects.filter(borrower=borrower).filter(status__exact='o').order_by('due_back')
        else:
            return BookInstance.objects.filter(status__exact='o').order_by('due_back')


class LanguageService(Service):
    def List(self, request, context):
        languages = Language.objects.all()
        serializer = LanguageProtoSerializer(languages, many=True)
        for msg in serializer.message:
            yield msg


class GenreService(Service):
    def List(self, request, context):
        genres = Genre.objects.all()
        serializer = LanguageProtoSerializer(genres, many=True)
        for msg in serializer.message:
            yield msg
