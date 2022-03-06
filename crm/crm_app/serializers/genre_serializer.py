from rest_framework import serializers
from ..models import GenreModel



class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenreModel
        fields = '__all__'
