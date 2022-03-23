from django.db import models
from django.contrib.postgres.fields import ArrayField


class MovieModel(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    adult = models.BooleanField(default=False)
    imdb_id = models.CharField(max_length=20, blank=True)
    language = models.CharField(max_length=5, blank=True)
    popularity = models.CharField(max_length=5, blank=True)
    poster_path = models.CharField(max_length=50, blank=True)
    release_date = models.CharField(max_length=15, blank=True)
    runtime = models.CharField(max_length=5, blank=True)
    spoken_languages = ArrayField(models.CharField(max_length=5), blank=True)
    status = models.CharField(max_length=10, blank=True)
    tagline = models.TextField(default="", blank=True)
    backdrop_path = models.CharField(max_length=50, blank=True)
    title = models.CharField(max_length=100, null=False, default="")
    overview = models.TextField(default="", blank=True)
    genres = ArrayField(models.CharField(max_length=20), null=True)
    production_companies = ArrayField(models.CharField(max_length=20), null=True)
    cast_members = ArrayField(models.CharField(max_length=20), null=True)
    keywords = ArrayField(models.CharField(max_length=30), null=True)

    class Meta:
        db_table = "movies"