from django.db import models


class MovieMovieRecomModel(models.Model):
    movie_id1 = models.CharField(max_length=15, null=False, default='')
    movie_id2 = models.CharField(max_length=15, null=False, default='')
    score = models.DecimalField(default=0, decimal_places=2, max_digits=7)

    class Meta:
        db_table = 'movie_to_movie2'