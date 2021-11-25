from django.db import models


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.TextField(unique=True)
    password = models.TextField()

