from django.db import models


class ProductionCompanyModel(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'production_company'