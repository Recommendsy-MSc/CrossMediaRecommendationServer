from rest_framework import serializers
from ..models import GlobalVarModel


class GlobalVarSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalVarModel
        fields = '__all__'