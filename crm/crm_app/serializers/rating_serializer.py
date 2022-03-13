from rest_framework import serializers
from ..models import MovieRatingModel, TvRatingModel


class MovieRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieRatingModel
        fields = '__all__'


class TvRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieRatingModel
        fields = '__all__'
