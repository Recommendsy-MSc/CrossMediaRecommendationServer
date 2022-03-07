from rest_framework import serializers
from ..models import TvModel, TvRecpModel



class TvSerializer(serializers.ModelSerializer):
    class Meta:
        model = TvModel
        fields = '__all__'

class TvRecpSerializer(serializers.ModelSerializer):
    class Meta:
        model = TvRecpModel
        fields = '__all__'


class BasicTvSerializer(serializers.ModelSerializer):
    class Meta:
        model = TvModel
        fields = ('id', 'title', 'poster_path')