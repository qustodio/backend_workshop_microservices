from django_grpc_framework.services import Service

from recomendations.models import (
    Author,
    BookInstance,
    Book,
    LibraryUser,
    UserRecomendation
)
from recomendations.serializers import BookProtoSerializer

class RecomendationService(Service):
    def List(self, request, context):
        user_id = request.id

        user = LibraryUser.objects.get(id=user_id)
        recomendations = self.calculate_recomendations(user=user)
        self.save_recomendations(
            recomended_books=recomendations,
            user=user
        )

        serializer = BookProtoSerializer(recomendations, many=True)
        for msg in serializer.message:
            yield msg

    def get_all_books(self):
        return Book.objects.all()

    def get_book(self, book_id):
        return Book.objects.filter(pk=book_id)

    def get_book_instances_from_user(self, user_id):
        user = LibraryUser.objects.get(pk=user_id)
        return BookInstance.objects.filter(borrower=user)

    def calculate_recomendations(
        self,
        user
    ):
        genres = BookInstance.objects.all()
        return books

    def save_recomendations(self, recomended_books, user):
       UserRecomendation.objects.create(
            user=user,
        ).books.set(recomended_books)

        