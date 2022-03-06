from django.db import models

class BookRatingModel(models.Model):
    user = models.ForeignKey('crm_app.UserModel', on_delete=models.CASCADE)
    book = models.CharField(max_length=20)
    rating = models.IntegerField(default=1)