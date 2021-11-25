from django.db import models
from django.contrib.auth.models import UserManager, AbstractUser



# Create your models here.
class LibraryUser(AbstractUser):
    objects = UserManager()

class Book(models.Model):
    pass

class UserRecomendation(models.Model):
    user = models.IntegerField()
    books = models.ManyToManyField(Book)
