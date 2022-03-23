from rest_framework import serializers
from ..models import BrokenLinkModel, InaccurateDataModel, InaccurateRecomModel, MissingTitleModel
from django.utils import timezone


class MissingTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MissingTitleModel
        fields = '__all__'

    def update(self, instance: MissingTitleModel, validated_data):
        instance.completed_date = timezone.now()
        instance.active = validated_data['active']
        instance.added = validated_data['added']
        instance.save()
        return instance

class InaccurateDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = InaccurateDataModel
        fields = '__all__'

    def update(self, instance: InaccurateDataModel, validated_data):
        instance.active = validated_data['active']
        instance.completed_date = timezone.now()
        instance.save()
        return instance


class InaccurateRecomSerializer(serializers.ModelSerializer):
    class Meta:
        model = InaccurateRecomModel
        fields = '__all__'

    def update(self, instance: InaccurateRecomModel, validated_data):
        instance.completed_date = timezone.now()
        instance.active = validated_data['active']
        instance.save()
        return instance


class BrokenLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrokenLinkModel
        fields = '__all__'

    def update(self, instance: BrokenLinkModel, validated_data):
        instance.completed_date = timezone.now()
        instance.active = validated_data['active']
        instance.save()
        return instance
