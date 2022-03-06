from rest_framework import viewsets
from ..models import GameModel
from django.db.models import QuerySet
from rest_framework.permissions import  AllowAny
from ..serializers import GameSerializer, GameRecpSerializer
from rest_framework.response import Response
from ..models import GameRecpModel
from ..helper import customResponse


class GameViewSet(viewsets.ModelViewSet):
    queryset: QuerySet = GameModel.objects.all()
    permission_classes = [AllowAny]
    serializer_class = GameSerializer

    def retrieve(self, request, *args, **kwargs):
        instance: GameModel = self.get_object()
        print(instance.id)
        serializer = self.get_serializer(instance)

        game_recp: GameRecpModel = GameRecpModel.objects.get(id=instance.id)

        response = serializer.data
        serializer = GameRecpSerializer(instance=game_recp)
        response.update(serializer.data)
        response.update({'media_type': '2'})

        return customResponse(True, response)