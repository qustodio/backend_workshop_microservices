from rest_framework import serializers

from recomendations.models import BookInstance


class BookInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookInstance
        fields = ['id', 'book', 'imprint', 'due_back', 'borrower', 'status']

    id = serializers.UUIDField(read_only=True, format='hex')