from django.db import models
from django.contrib.postgres.fields import ArrayField


class GameRecpModel(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    tags = ArrayField(models.CharField(max_length=20))
    publishers = ArrayField(models.CharField(max_length=20))
    genres = ArrayField(models.CharField(max_length=20))
    esrb_rating = models.CharField(max_length=20)

    class Meta:
        db_table = "games_recp"