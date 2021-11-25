from django_grpc_framework.services import Service

from recomendations.models import (
    BookInstance,
    Book,
    UserRecomendation
)
from recomendations.serializers import BookRecomendationProtoSerializer

class RecomendationService(Service):
    def List(self, request, context):
        user_id = request.id

        recomendations = self.calculate_recomendations(user=user_id)
        self.save_recomendations(
            recomended_books=recomendations,
            user=user_id
        )

        serializer = BookRecomendationProtoSerializer(recomendations, many=True)
        for msg in serializer.message:
            yield msg

    def get_all_books(self):
        return Book.objects.all()

    def get_book(self, book_id):
        return Book.objects.filter(pk=book_id)

    def get_book_instances_from_user(self, user_id):
        return BookInstance.objects.filter(borrower=user_id)

    def calculate_recomendations(
        self,
        user
    ):
        read_books = BookInstance.objects.filter(
            borrower=user
        ).prefetch_related('book', 'book_author')
        authors = read_books.values('book__author')

        recomendations = Book.objects.filter(
            author__in=authors
        ).exclude(
            id__in=read_books.values('book__id')
        )

        if len(recomendations) == 0:
            recomendations = Book.objects.all().exclude(
                id__in=read_books.values('book__id')
            )[:2]
        
        return recomendations

    def save_recomendations(self, recomended_books, user):
       UserRecomendation.objects.create(
            user=user,
        ).books.set(recomended_books)

        