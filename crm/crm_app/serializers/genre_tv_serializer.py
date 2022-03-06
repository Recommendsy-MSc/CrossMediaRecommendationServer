from rest_framework import serializers
from ..models import TvGenreModel



class GenreTvSerializer(serializers.ModelSerializer):
    class Meta:
        model = TvGenreModel
        fields = '__all__'
