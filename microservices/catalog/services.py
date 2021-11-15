import grpc
from django_grpc_framework.services import Service

from catalog.models import Book
from catalog.serializers import BookProtoSerializer


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
            self.context.abort(grpc.StatusCode.NOT_FOUND, 'Post:%s not found!' % pk)

    def Update(self, request, context):
        post = self.get_object(request.id)
        serializer = BookProtoSerializer(post, message=request)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.message
