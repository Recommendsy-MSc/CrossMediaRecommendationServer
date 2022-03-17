from rest_framework import serializers
from ..models import TvModel, TvRecpModel
from django.db import models
from .genre_tv_serializer import GenreTvSerializer



class TvSerializer(serializers.ModelSerializer):
    title_type = serializers.IntegerField(default=1)

    class Meta:
        model = TvModel
        fields = '__all__'
        extra_fields = ('title_type', )


class TvRecpSerializer(serializers.ModelSerializer):
    class Meta:
        model = TvRecpModel
        fields = '__all__'


class BasicTvSerializer(serializers.ModelSerializer):
    title_type = serializers.IntegerField(default=1)

    class Meta:
        model = TvModel
        fields = ('id', 'title', 'poster_path', 'title_type', )