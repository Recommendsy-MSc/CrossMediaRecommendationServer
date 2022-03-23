from django.db import models
from django.utils import timezone

class MyListModel(models.Model):
    user = models.ForeignKey('UserModel', on_delete=models.CASCADE)
    title = models.CharField(max_length=10)
    title_type = models.IntegerField(default=0)
    created_date = models.DateTimeField(default=timezone.now)

class MovieListModel(models.Model):
    user = models.ForeignKey('UserModel', on_delete=models.CASCADE)
    movie = models.CharField(max_length=10)


class TvListModel(models.Model):
    user = models.ForeignKey('UserModel', on_delete=models.CASCADE)
    tv = models.CharField(max_length=10)




