from django.db import models

class MovieRatingModel(models.Model):
    user = models.ForeignKey('crm_app.UserModel', on_delete=models.CASCADE)
    movie = models.CharField(max_length=20)
    rating = models.IntegerField(default=1)
