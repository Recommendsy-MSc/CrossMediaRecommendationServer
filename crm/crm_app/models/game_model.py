from django.db import models
from django.contrib.postgres.fields import ArrayField


class GameModel(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    available_at = ArrayField(models.CharField(max_length=15))
    release = models.CharField(max_length=10)
    background_image = models.CharField(max_length=100)
    website = models.CharField(max_length=100)
    screenshots = ArrayField(models.CharField(max_length=100))
    platforms = ArrayField(models.CharField(max_length=10))

    class Meta:
        db_table = "games"