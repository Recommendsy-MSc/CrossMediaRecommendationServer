from django.db import models
from django.contrib.postgres.fields import ArrayField


class CastModel(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=30)
    profile_path = models.CharField(max_length=50)
    popularity = models.CharField(max_length=5)

    class Meta:
        db_table = "cast_members"