from django_grpc_framework.services import Service

from recommendations.models import (
    BookInstance,
    Book,
    UserRecommendation
)
from recommendations.serializers import BookRecommendationProtoSerializer

class RecommendationService(Service):
    def List(self, request, context):
        user_id = request.id

        recommendations = self.calculate_recommendations(user=user_id)
        self.save_recommendations(
            recommended_books=recommendations,
            user=user_id
        )

        serializer = BookRecommendationProtoSerializer(recommendations, many=True)
        for msg in serializer.message:
            yield msg

    def get_all_books(self):
        return Book.objects.all()

    def get_book(self, book_id):
        return Book.objects.filter(pk=book_id)

    def get_book_instances_from_user(self, user_id):
        return BookInstance.objects.filter(borrower=user_id)

    def calculate_recommendations(
        self,
        user
    ):
        read_books = BookInstance.objects.filter(
            borrower=user
        ).prefetch_related('book', 'book_author')
        authors = read_books.values('book__author')

        recommendations = Book.objects.filter(
            author__in=authors
        ).exclude(
            id__in=read_books.values('book__id')
        )

        if len(recommendations) == 0:
            recommendations = Book.objects.all().exclude(
                id__in=read_books.values('book__id')
            )[:2]
        
        return recommendations

    def save_recommendations(self, recommended_books, user):
       UserRecommendation.objects.create(
            user=user,
        ).books.set(recommended_books)

        