from django.db import models


class TvGenreModel(models.Model):
    id = models.CharField(max_length=101, primary_key=True)
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'genres_tv'