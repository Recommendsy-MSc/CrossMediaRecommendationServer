from django.db import models


class MovieTvRecomModel(models.Model):
    movie_id = models.CharField(max_length=15)
    tv_id = models.CharField(max_length=15)
    score = models.DecimalField(default=0, decimal_places=2, max_digits=7,)

    class Meta:
        db_table = 'movie_to_tv'