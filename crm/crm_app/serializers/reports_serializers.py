from rest_framework import serializers
from ..models import BrokenLinkModel, InaccurateDataModel, InaccurateRecomModel


class InaccurateDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = InaccurateDataModel
        fields = '__all__'


class InaccurateRecomSerializer(serializers.ModelSerializer):
    class Meta:
        model = InaccurateRecomModel
        fields = '__all__'


class BrokenLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrokenLinkModel
        fields = '__all__'
