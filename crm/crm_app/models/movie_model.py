from django.db import models
from django.contrib.postgres.fields import ArrayField


class MovieModel(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    adult = models.BooleanField(default=False)
    imdb_id = models.CharField(max_length=20)
    language = models.CharField(max_length=5)
    popularity = models.CharField(max_length=5)
    poster_path = models.CharField(max_length=50)
    release_date = models.CharField(max_length=15)
    runtime = models.CharField(max_length=5)
    spoken_languages = ArrayField(models.CharField(max_length=5))
    status = models.CharField(max_length=10)
    tagline = models.TextField(default="", blank=True)
    backdrop_path = models.CharField(max_length=50)
    title = models.CharField(max_length=100, null=False, default="")
    overview = models.TextField(default="")
    genres = ArrayField(models.CharField(max_length=20), null=True)
    production_companies = ArrayField(models.CharField(max_length=20), null=True)
    cast_members = ArrayField(models.CharField(max_length=20), null=True)
    keywords = ArrayField(models.CharField(max_length=30), null=True)

    class Meta:
        db_table = "movies"