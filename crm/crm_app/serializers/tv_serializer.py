from rest_framework import serializers
from ..models import TvModel, TvRecpModel, TvRatingModel, MyListModel
from django.db import models
from .genre_tv_serializer import GenreTvSerializer
from rest_framework.request import Request
from django.db.models import Q



class TvSerializer(serializers.ModelSerializer):
    title_type = serializers.IntegerField(default=1)

    class Meta:
        model = TvModel
        fields = '__all__'
        extra_fields = ('title_type', )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request: Request = self.context.get('request')
        if request and hasattr(request, 'user'):
            if not request.user.id is None:
                query_user = Q(user__exact=request.user)
                query_tv = Q(tv__exact=data['id'])
                try:
                    rated: TvRatingModel = TvRatingModel.objects.get(query_tv & query_user)
                    data['user_rating'] = rated.rating
                except TvRatingModel.DoesNotExist:
                    pass

                query_type = Q(title_type__exact=1)
                query_title = Q(title__exact=data['id'])
                try:
                    listed: MyListModel = MyListModel.objects.get(query_type & query_title & query_user)
                    data['added'] = True
                except MyListModel.DoesNotExist:
                    data['added'] = False
        return data



class TvRecpSerializer(serializers.ModelSerializer):
    class Meta:
        model = TvRecpModel
        fields = '__all__'


class BasicTvSerializer(serializers.ModelSerializer):
    title_type = serializers.IntegerField(default=1)

    class Meta:
        model = TvModel
        fields = ('id', 'title', 'poster_path', 'title_type', )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request: Request = self.context.get('request')
        if request and hasattr(request, 'user'):
            if not request.user.id is None:
                query_user = Q(user__exact=request.user)
                query_tv = Q(tv__exact=data['id'])
                try:
                    rated: TvRatingModel = TvRatingModel.objects.get(query_tv & query_user)
                    data['user_rating'] = rated.rating
                except TvRatingModel.DoesNotExist:
                    pass

                query_type = Q(title_type__exact=1)
                query_title = Q(title__exact=data['id'])
                try:
                    listed: MyListModel = MyListModel.objects.get(query_type & query_title & query_user)
                    data['added'] = True
                except MyListModel.DoesNotExist:
                    data['added'] = False
                    
        return data