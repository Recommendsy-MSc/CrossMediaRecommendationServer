from rest_framework import viewsets
from ..models import TvGenreModel
from ..serializers import GenreTvSerializer
from rest_framework.permissions import AllowAny
from ..helper import customResponse


class TvGenreViewSet(viewsets.ModelViewSet):
    queryset = TvGenreModel.objects.all()
    permission_classes = [AllowAny]
    serializer_class = GenreTvSerializer

    def list(self, request, *args, **kwargs):
        return customResponse(True, super().list(self, request, *args, **kwargs).data)