# Generated by Django 4.0.3 on 2022-03-08 05:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0009_rename_movie_moviemovierecommodel_movie_id1_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='moviemovierecommodel',
            old_name='movie_id1',
            new_name='movie',
        ),
    ]
