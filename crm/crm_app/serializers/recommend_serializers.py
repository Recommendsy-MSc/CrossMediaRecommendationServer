from rest_framework import serializers
from ..models import MovieMovieRecomModel, MovieTvRecomModel, TvTvRecomModel, RecomMovieBookModel


class TvTvSerializer(serializers.ModelSerializer):
    class Meta:
        model = TvTvRecomModel
        fields = '__all__'


class MovieMovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = MovieMovieRecomModel
        fields = '__all__'


class MovieTvSerializer(serializers.ModelSerializer):

    class Meta:
        model = MovieTvRecomModel
        fields = '__all__'

class MovieBookSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecomMovieBookModel
        fields = '__all__'