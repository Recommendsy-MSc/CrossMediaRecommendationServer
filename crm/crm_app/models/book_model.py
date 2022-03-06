from django.db import models

class BookModel(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    date_published = models.CharField(max_length=15)
    publisher = models.CharField(max_length=50)
    description = models.TextField()
    link = models.CharField(max_length=100)
    cover_link = models.CharField(max_length=100)
    amazon_link = models.CharField(max_length=100)
    content_rating = models.CharField(max_length=5)
    isbn_id = models.CharField(max_length=15)

    class Meta:
        db_table = "books"