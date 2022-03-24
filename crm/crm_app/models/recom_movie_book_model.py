from django.db import models

class RecomMovieBookModel(models.Model):
    book_id = models.CharField(max_length=15, blank=True)
    movie_id = models.CharField(max_length=15, blank=True)
    score = models.IntegerField(default=0)
    valid = models.BooleanField(default=True)

    class Meta:
        db_table = 'movie_to_book'