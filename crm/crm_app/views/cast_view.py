from rest_framework import viewsets
from django.db.models import QuerySet
from rest_framework.permissions import  AllowAny
from ..serializers import CastSerializer
from rest_framework.response import Response
from ..models import CastModel
from ..helper import customResponse


class CastViewSet(viewsets.ModelViewSet):
    queryset: QuerySet = CastModel.objects.all()
    permission_classes = [AllowAny]
    serializer_class = CastSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return customResponse(True, serializer.data)