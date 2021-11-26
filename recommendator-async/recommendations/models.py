import uuid

from django.db import models
from dj_cqrs.mixins import ReplicaMixin


class Genre(models.Model):
    CQRS_ID = 'genre'
    name = models.CharField(
        max_length=200,
    )


class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(max_length=200)
    author = models.IntegerField(null=False, blank=False)
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField('ISBN', max_length=13,
                            unique=True,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn'
                                      '">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
    language = models.IntegerField()

class BookInstance(ReplicaMixin, models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
    CQRS_ID = 'book_instance'
    CQRS_SERIALIZER = 'recommendat.serializers.BookInstanceSerializer'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey(Book, on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.IntegerField(null=True)

    @property
    def pk(self):
        return super().pk.hex

    LOAN_STATUS = (
        ('d', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    @classmethod
    def cqrs_create(cls, sync, mapped_data, previous_data=None):
        mapped_data['book'] = Book.objects.get(id=mapped_data['book'])
        super().cqrs_create(sync, mapped_data, previous_data)
        
    def cqrs_update(self, sync, mapped_data, previous_data=None):
        mapped_data['book'] = Book.objects.get(id=mapped_data['book'])
        super().cqrs_update(sync, mapped_data, previous_data)

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='d',
        help_text='Book availability')

    def __str__(self):
        """String for representing the Model object."""
        return '{0} ({1})'.format(self.id, self.book.title)


class UserRecommendation(models.Model):
    user = models.IntegerField(null=False, blank=False)
    books = models.ManyToManyField(Book)
