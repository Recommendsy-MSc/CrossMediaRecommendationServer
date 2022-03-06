from rest_framework import viewsets
from ..models import GenreModel
from ..serializers import GenreSerializer
from rest_framework.permissions import AllowAny
from ..helper import customResponse


class GenreViewSet(viewsets.ModelViewSet):
    queryset = GenreModel.objects.all()
    permission_classes = [AllowAny]
    serializer_class = GenreSerializer

    def list(self, request, *args, **kwargs):
        return customResponse(True, super().list(self, request, *args, **kwargs).data)