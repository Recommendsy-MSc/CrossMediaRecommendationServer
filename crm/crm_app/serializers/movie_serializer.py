from rest_framework import serializers
from ..models import MovieModel, MovieRecpModel
from .rating_serializer import MovieRatingSerializer
from django.db import models



class MovieSerializer(serializers.ModelSerializer):
    title_type = serializers.IntegerField(default=0)
    class Meta:
        model = MovieModel
        fields = '__all__'
        extra_fields = ('title_type', )


class MovieRecpSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieRecpModel
        fields = '__all__'


class BasicMovieSerializer(serializers.ModelSerializer):
    title_type = serializers.IntegerField(default=0)
    class Meta:
        model = MovieModel
        fields = ('id', 'title', 'poster_path', 'title_type', )


# class BasicMovieSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = MovieModel
#         fields = ('poster_path', )
#
#
# class BasicMovieRecpSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = MovieRecpModel
#         fields = ('title', )
#
#
# class MovieTileSerializer(serializers.ModelSerializer):
#     movie = BasicMovieSerializer()
#     recp = BasicMovieRecpSerializer()
#
#     class Meta:
#         model = BasicMovieModel
#         fields = ('movie', 'recp')


