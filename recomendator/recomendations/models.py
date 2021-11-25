from django.db import models

class Book(models.Model):
    pass

class UserRecomendation(models.Model):
    user = models.IntegerField()
    books = models.ManyToManyField(Book)
