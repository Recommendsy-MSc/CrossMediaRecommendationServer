from rest_framework import serializers
from ..models import MovieRatingModel


class MovieRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieRatingModel
        fields = '__all__'