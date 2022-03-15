from django.db import models
from django.utils import timezone

class InaccurateDataModel(models.Model):
    user = models.ForeignKey('crm_app.UserModel', on_delete=models.CASCADE)
    title = models.CharField(max_length=15, null=False, default='')
    type = models.IntegerField(default=0)
    note = models.TextField(default='')
    created_date = models.DateTimeField(default=timezone.now)


class InaccurateRecomModel(models.Model):
    title = models.CharField(max_length=15, null=False, default='')
    recommended_title = models.CharField(max_length=15, null=False, default='')
    created_date = models.DateTimeField(default=timezone.now)
    count = models.IntegerField(default=1)

    # 0 for movies, 1 for TV
    type = models.IntegerField(default=0)
    recommended_type = models.IntegerField(default=0)


class BrokenLinkModel(models.Model):
    title = models.CharField(max_length=15, null=False, default='')
    created_date = models.DateTimeField(default=timezone.now)
    count = models.IntegerField(default=1)
    type = models.IntegerField(default=0)