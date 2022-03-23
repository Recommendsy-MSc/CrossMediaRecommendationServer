from django.db import models
from django.contrib.postgres.fields import ArrayField


class TvModel(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    in_production = models.BooleanField(default=False)
    last_air_date = models.CharField(max_length=15, blank=True)
    no_episodes = models.IntegerField(blank=True)
    no_seasons = models.IntegerField(blank=True)
    original_language = models.CharField(max_length=5, blank=True)
    poster_path = models.CharField(max_length=50, blank=True)
    spoken_languages = ArrayField(models.CharField(max_length=5, blank=True))
    status = models.CharField(max_length=10, blank=True)
    tagline = models.TextField(blank=True, default="")
    title = models.CharField(max_length=100, default="")
    overview = models.TextField(null=True, blank=True)
    genres = ArrayField(models.CharField(max_length=20), null=True)
    production_companies = ArrayField(models.CharField(max_length=20), null=True)
    keywords = ArrayField(models.CharField(max_length=20), null=True)
    type = models.CharField(max_length=10, null=True)
    cast_members = ArrayField(models.CharField(max_length=20), null=True)

    class Meta:
        db_table = "tv"