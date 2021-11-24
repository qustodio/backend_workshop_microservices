import uuid

from django.db import models
from django.contrib.auth.models import UserManager, AbstractUser
from dj_cqrs.mixins import ReplicaMixin



# Create your models here.
class LibraryUser(ReplicaMixin, AbstractUser):
    CQRS_ID = 'user'
    objects = UserManager()


class Genre(ReplicaMixin, models.Model):
    """Model representing a book genre (e.g. Science Fiction, Non Fiction)."""
    CQRS_ID = 'genre'

    name = models.CharField(
        max_length=200,
        help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)"
        )

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name


class Book(ReplicaMixin, models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    CQRS_ID = 'book'

    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in file.
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField('ISBN', max_length=13,
                            unique=True,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn'
                                      '">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
    # ManyToManyField used because a genre can contain many books and a Book can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    language = models.IntegerField()
    
    class Meta:
        ordering = ['title', 'author']

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    @classmethod
    def cqrs_create(cls, sync, mapped_data, previous_data=None):
        mapped_data['author'] = Author.objects.get(id=mapped_data['author'])
        super().cqrs_create(sync, mapped_data, previous_data)

    def cqrs_update(self, sync, mapped_data, previous_data=None):
        mapped_data['author'] = Author.objects.get(id=mapped_data['author'])
        super().cqrs_update(sync, mapped_data, previous_data)

class BookInstance(ReplicaMixin, models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
    CQRS_ID = 'book_instance'
    CQRS_SERIALIZER = 'recomendat.serializers.BookInstanceSerializer'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey(Book, on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(LibraryUser, on_delete=models.SET_NULL, null=True, blank=True)

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
        if mapped_data['borrower']:
            mapped_data['borrower'] = LibraryUser.objects.get(id=mapped_data['borrower'])
        super().cqrs_create(sync, mapped_data, previous_data)
        
    def cqrs_update(self, sync, mapped_data, previous_data=None):
        mapped_data['book'] = Book.objects.get(id=mapped_data['book'])
        if mapped_data['borrower']:
            mapped_data['borrower'] = LibraryUser.objects.get(id=mapped_data['borrower'])
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


class Author(ReplicaMixin, models.Model):
    """Model representing an author."""
    CQRS_ID = 'author'

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('died', null=True, blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return '{0}, {1}'.format(self.last_name, self.first_name)

class UserRecomendation(models.Model):
    user = models.ForeignKey(LibraryUser, on_delete=models.CASCADE, null=False)
    books = models.ManyToManyField(Book)
