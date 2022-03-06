from rest_framework import viewsets
from ..models import BookModel
from django.db.models import QuerySet
from rest_framework.permissions import  AllowAny
from ..serializers import BookSerializer, BookRecpSerializer
from rest_framework.response import Response
from ..models import BookRecpModel
from ..helper import customResponse


class BookViewSet(viewsets.ModelViewSet):
    queryset: QuerySet = BookModel.objects.all()
    permission_classes = [AllowAny]
    serializer_class = BookSerializer

    def retrieve(self, request, *args, **kwargs):
        instance: BookModel = self.get_object()
        print(instance.id)
        serializer = self.get_serializer(instance)

        book_recp: BookRecpModel = BookRecpModel.objects.get(id=instance.id)

        response = serializer.data
        serializer = BookRecpSerializer(instance=book_recp)
        response.update(serializer.data)
        response.update({'media_type': '3'})
        return customResponse(True, response)