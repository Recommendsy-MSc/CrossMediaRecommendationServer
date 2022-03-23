from rest_framework import serializers
from ..models import MovieRatingModel, TvRatingModel, BookRatingModel


class MovieRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieRatingModel
        fields = '__all__'


class TvRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TvRatingModel
        fields = '__all__'

class BookRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookRatingModel
        fields = '__all__'
