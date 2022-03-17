from django.db import models


class TvTvRecomModel(models.Model):
    tv_id1 = models.CharField(max_length=15, null=False, default='')
    tv_id2 = models.CharField(max_length=15, null=False, default='')
    score = models.DecimalField(default=0, decimal_places=2, max_digits=7)
    valid = models.BooleanField(default=True)

    class Meta:
        db_table = 'tv_to_tv'