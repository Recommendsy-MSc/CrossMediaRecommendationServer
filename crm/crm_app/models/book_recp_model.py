from django.db import models
from django.contrib.postgres.fields import ArrayField


class BookRecpModel(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    title = models.CharField(max_length=200)
    series = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    genres = ArrayField(models.CharField(max_length=20))

    class Meta:
        db_table = "books_recp"