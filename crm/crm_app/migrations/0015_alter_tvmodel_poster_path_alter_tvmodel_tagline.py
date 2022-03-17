# Generated by Django 4.0.3 on 2022-03-17 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0014_alter_moviemodel_tagline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tvmodel',
            name='poster_path',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='tvmodel',
            name='tagline',
            field=models.TextField(blank=True, default=''),
        ),
    ]
