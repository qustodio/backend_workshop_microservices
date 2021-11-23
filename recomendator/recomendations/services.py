from django_grpc_framework.services import Service

from recomendations.models import Book
from recomendations.serializers import BookProtoSerializer

class RecomendationService(Service):
    def List(self, request, context):
        books = Book.objects.all()
        serializer = BookProtoSerializer(books, many=True)
        for msg in serializer.message:
            yield msg