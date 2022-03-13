from django.db import models

class MovieListModel(models.Model):
    user = models.ForeignKey('UserModel', on_delete=models.CASCADE)
    movie = models.CharField(max_length=10)


class TvListModel(models.Model):
    user = models.ForeignKey('UserModel', on_delete=models.CASCADE)
    tv = models.CharField(max_length=10)




