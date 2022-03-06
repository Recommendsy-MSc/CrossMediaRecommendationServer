from django.db import models
from django.contrib.postgres.fields import ArrayField


class UserGenreModel(models.Model):
    genre_list = ArrayField(models.CharField(max_length=25), blank=True)
    user = models.ForeignKey('crm_app.UserModel', blank=False, null=False, on_delete=models.CASCADE)

