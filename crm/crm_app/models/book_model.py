from django.db import models
from django.contrib.postgres.fields import ArrayField


class BookModel(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    title = models.CharField(max_length=100, blank=True)
    series = models.CharField(max_length=100, blank=True)
    author = models.CharField(max_length=100, blank=True)
    date_published = models.CharField(max_length=15,)
    publisher = models.CharField(max_length=50)
    genres = ArrayField(models.CharField(max_length=30, default=''), null=True)

    overview = models.TextField()
    link = models.CharField(max_length=100)
    cover_link = models.CharField(max_length=100)
    amazon_redirect_link = models.CharField(max_length=100)
    content_rating = models.CharField(max_length=5)
    isbn = models.CharField(max_length=15)

    class Meta:
        db_table = "books"