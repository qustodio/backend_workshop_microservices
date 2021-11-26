from django.db import models

class Book(models.Model):
    pass

class UserRecommendation(models.Model):
    user = models.IntegerField()
    books = models.ManyToManyField(Book)
