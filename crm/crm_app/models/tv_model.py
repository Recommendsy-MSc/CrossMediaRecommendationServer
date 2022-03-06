from django.db import models
from django.contrib.postgres.fields import ArrayField


class TvModel(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    in_production = models.BooleanField(default=False)
    last_air_date = models.CharField(max_length=15)
    no_episodes = models.IntegerField()
    no_seasons = models.IntegerField()
    original_language = models.CharField(max_length=5)
    poster_path = models.CharField(max_length=30)
    spoken_languages = ArrayField(models.CharField(max_length=5))
    status = models.CharField(max_length=10)
    tagline = models.TextField()
    title = models.CharField(max_length=100, default="")
    overview = models.TextField(null=True)
    genres = ArrayField(models.CharField(max_length=20), null=True)
    production_companies = ArrayField(models.CharField(max_length=20), null=True)
    keywords = ArrayField(models.CharField(max_length=20), null=True)
    type = models.CharField(max_length=10, null=True)
    cast_member = ArrayField(models.CharField(max_length=20), null=True)

    class Meta:
        db_table = "tv"