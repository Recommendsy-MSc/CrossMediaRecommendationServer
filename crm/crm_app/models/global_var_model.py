from django.db import models


class GlobalVarModel(models.Model):
    name = models.CharField(max_length=30)
    value = models.CharField(max_length=100)

    class Meta:
        db_table = 'crm_app_globalvarmodel'