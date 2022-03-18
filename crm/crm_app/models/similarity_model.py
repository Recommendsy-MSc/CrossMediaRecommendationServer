from django.db import models

class SimilarityModel(models.Model):
    user1 = models.ForeignKey('crm_app.UserModel', on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey('crm_app.UserModel', on_delete=models.CASCADE, related_name='user2')
    similarity = models.DecimalField(max_digits=3, decimal_places=2)