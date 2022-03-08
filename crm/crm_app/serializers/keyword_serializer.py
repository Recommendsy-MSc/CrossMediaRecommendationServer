from rest_framework import serializers
from ..models import KeywordModel

class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeywordModel
        fields = '__all__'