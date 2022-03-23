from django.db import models
from django.utils import timezone



class MissingTitleModel(models.Model):
    title = models.CharField(max_length=100, default='')
    user = models.ForeignKey('crm_app.UserModel', on_delete=models.CASCADE)
    title_type = models.IntegerField(default=0)
    created_date = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)
    added = models.CharField(max_length=15, null=True, blank=True)
    completed_date = models.DateTimeField(null=True)


class InaccurateDataModel(models.Model):
    user = models.ForeignKey('crm_app.UserModel', on_delete=models.CASCADE)
    title = models.CharField(max_length=15, null=False, default='')
    type = models.IntegerField(default=0)
    note = models.TextField(default='')
    created_date = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)
    # name = models.CharField(max_length=100, null=False, default='')
    completed_date = models.DateTimeField(null=True)



class InaccurateRecomModel(models.Model):
    title = models.CharField(max_length=15, null=False, default='')
    recommended_title = models.CharField(max_length=15, null=False, default='')
    created_date = models.DateTimeField(default=timezone.now)
    count = models.IntegerField(default=1)
    # name = models.CharField(max_length=100, null=False, default='')
    # recommended_name = models.CharField(max_length=100, null=False, default='')
    # 0 for movies, 1 for TV
    type = models.IntegerField(default=0)
    recommended_type = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    completed_date = models.DateTimeField(null=True)



class BrokenLinkModel(models.Model):
    title = models.CharField(max_length=15, null=False, default='')
    created_date = models.DateTimeField(default=timezone.now)
    count = models.IntegerField(default=1)
    type = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    completed_date = models.DateTimeField(null=True)

