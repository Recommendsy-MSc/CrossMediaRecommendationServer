# Generated by Django 4.0.3 on 2022-03-08 05:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0007_genremodel_keywordmodel_tvgenremodel_and_more'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='moviemovierecommodel',
            table='movie_to_movie',
        ),
        migrations.AlterModelTable(
            name='movietvrecommodel',
            table='movie_to_tv',
        ),
    ]
