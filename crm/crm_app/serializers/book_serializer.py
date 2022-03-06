from rest_framework import serializers
from ..models import BookModel, BookRecpModel


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookModel
        fields = '__all__'


class BookRecpSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookRecpModel
        fields = '__all__'