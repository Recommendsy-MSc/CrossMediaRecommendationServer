from rest_framework import viewsets
from rest_framework.request import Request, QueryDict
from ..models import InaccurateDataModel, InaccurateRecomModel, BrokenLinkModel
from ..serializers import InaccurateDataSerializer, InaccurateRecomSerializer, BrokenLinkSerializer
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from ..helper import customResponse
from django.db.models import QuerySet, Q, Count
from ..serializers import MovieSerializer, TvSerializer
from ..models import MovieModel, TvModel


class InaccurateDataView(viewsets.ModelViewSet):
    queryset = InaccurateDataModel.objects.all()
    permission_classes = [AllowAny]
    serializer_class = InaccurateDataSerializer

    def create(self, request, *args, **kwargs):
        return customResponse(False, {"error": "Not Allowed"})

    def list(self, request, *args, **kwargs):
        return customResponse(False, {"error": "Not Allowed"})

    def update(self, request, *args, **kwargs):
        return customResponse(False, {"error": "Not Allowed"})

    def destroy(self, request, *args, **kwargs):
        return customResponse(False, {"error": "Not Allowed"})

    @action(detail=False, methods=['GET'])
    def get_latest(self, request: Request, *args, **kwargs):
        self.queryset = self.queryset.order_by('-created_date')
        serializer = self.serializer_class(self.queryset, many=True)
        return customResponse(True, serializer.data)


class InaccurateRecomView(viewsets.ModelViewSet):
    queryset = InaccurateRecomModel.objects.all()
    permission_classes = [AllowAny]
    serializer_class = InaccurateRecomSerializer

    def list(self, request: Request, *args, **kwargs):
        self.queryset = self.queryset.order_by('-count')
        return customResponse(True, InaccurateRecomSerializer(self.queryset, many=True).data)

class BrokenLinkView(viewsets.ModelViewSet):
    queryset = BrokenLinkModel.objects.all()
    permission_classes = [AllowAny]
    serializer_class = BrokenLinkSerializer

    def list(self, request: Request, *args, **kwargs):
        self.queryset = self.queryset.order_by('-count')
        return customResponse(True, BrokenLinkSerializer(self.queryset, many=True).data)

