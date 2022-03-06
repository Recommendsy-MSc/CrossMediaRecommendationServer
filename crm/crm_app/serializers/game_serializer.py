from rest_framework import serializers
from ..models import GameModel, GameRecpModel



class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameModel
        fields = '__all__'


class GameRecpSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameRecpModel
        fields = '__all__'