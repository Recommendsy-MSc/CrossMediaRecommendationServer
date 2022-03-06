from django.db import models

class StandardUnitsModel(models.Model):
    user = models.ForeignKey('crm_app.UserModel', on_delete=models.CASCADE)
    title_id = models.CharField(max_length=20)
    title_type = models.IntegerField()
    su = models.DecimalField(max_digits=3, decimal_places=2, default=0)