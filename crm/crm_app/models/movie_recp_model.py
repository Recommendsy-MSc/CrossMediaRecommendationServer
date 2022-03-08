from django.db import models
from django.contrib.postgres.fields import ArrayField


class MovieRecpModel(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    title = models.CharField(max_length=100)
    overview = models.TextField()
    genres = ArrayField(models.CharField(max_length=20))
    production_companies = ArrayField(models.CharField(max_length=20))
    cast_members = ArrayField(models.CharField(max_length=20))
    keywords = ArrayField(models.CharField(max_length=30))

    class Meta:
        db_table = "movies_recp"