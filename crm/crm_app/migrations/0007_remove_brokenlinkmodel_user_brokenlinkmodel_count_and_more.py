# Generated by Django 4.0.3 on 2022-03-15 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0006_inaccuraterecommodel_recommended_type_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='brokenlinkmodel',
            name='user',
        ),
        migrations.AddField(
            model_name='brokenlinkmodel',
            name='count',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='brokenlinkmodel',
            name='type',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='inaccuratedatamodel',
            name='type',
            field=models.IntegerField(default=0),
        ),
    ]
