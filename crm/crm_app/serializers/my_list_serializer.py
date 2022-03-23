from rest_framework import serializers
from ..models import MovieListModel, TvListModel, MyListModel


class MyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyListModel
        fields = '__all__'



class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieListModel
        fields = '__all__'


class TvListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TvListModel
        fields = '__all__'
