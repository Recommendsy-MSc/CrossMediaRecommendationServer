from django.db import models
from django.contrib.postgres.fields import ArrayField


class GameModel(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    title = models.CharField(max_length=100, null=True)
    overview = models.TextField(default='')
    genres = ArrayField(models.CharField(max_length=30), null=True)
    tags = ArrayField(models.CharField(max_length=30), null=True)
    esrb_rating = models.CharField(max_length=5, default='')
    publisher = ArrayField(models.CharField(max_length=30), null=True)
    keywords = ArrayField(models.CharField(max_length=30), null=True)
    release = models.CharField(max_length=10, null=True)
    website = models.CharField(max_length=100, null=True)
    available_at = ArrayField(models.CharField(max_length=15), null=True)
    background_image = models.CharField(max_length=100, null=True)
    website = models.CharField(max_length=100, null=True)
    screenshots = ArrayField(models.CharField(max_length=100), null=True)
    platforms = ArrayField(models.CharField(max_length=10), null=True)

    class Meta:
        db_table = "games"