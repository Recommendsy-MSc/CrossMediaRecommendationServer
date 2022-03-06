from django.db import models

class GameRatingModel(models.Model):
    user = models.ForeignKey('crm_app.UserModel', on_delete=models.CASCADE)
    game = models.CharField(max_length=20)
    rating = models.IntegerField(default=1)