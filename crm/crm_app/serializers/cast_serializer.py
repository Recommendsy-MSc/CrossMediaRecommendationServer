from rest_framework import serializers
from ..models import CastModel


class CastSerializer(serializers.ModelSerializer):
    class Meta:
        model = CastModel
        fields = '__all__'