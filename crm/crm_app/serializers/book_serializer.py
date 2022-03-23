from rest_framework import serializers
from ..models import BookModel, BookRatingModel, MyListModel
from rest_framework.request import Request
from django.db.models import Q


class BookSerializer(serializers.ModelSerializer):
    title_type = serializers.IntegerField(default=3)

    class Meta:
        model = BookModel
        fields = '__all__'
        extra_fields = ('title_type', )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request: Request = self.context.get('request')
        if request and hasattr(request, 'user'):
            if not request.user.id is None:
                query_user = Q(user__exact=request.user)
                query_book = Q(book__exact=data['id'])
                try:
                    rated: BookRatingModel = BookRatingModel.objects.get(query_book & query_user)
                    data['user_rating'] = rated.rating
                except BookRatingModel.DoesNotExist:
                    pass

                query_type = Q(title_type__exact=3)
                query_title = Q(title__exact=data['id'])
                try:
                    listed: MyListModel = MyListModel.objects.get(query_type & query_title & query_user)
                    data['added'] = True
                except MyListModel.DoesNotExist:
                    data['added'] = False
        return data

class BasicBookSerializer(serializers.ModelSerializer):
    title_type = serializers.IntegerField(default=3)
    class Meta:
        model = BookModel
        fields = ('id', 'cover_link', 'title', 'title_type')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request: Request = self.context.get('request')
        if request and hasattr(request, 'user'):
            if not request.user.id is None:
                query_user = Q(user__exact=request.user)
                query_book = Q(book__exact=data['id'])
                try:
                    rated: BookRatingModel = BookRatingModel.objects.get(query_book & query_user)
                    data['user_rating'] = rated.rating
                except BookRatingModel.DoesNotExist:
                    pass

                query_type = Q(title_type__exact=3)
                query_title = Q(title__exact=data['id'])
                try:
                    listed: MyListModel = MyListModel.objects.get(query_type & query_title & query_user)
                    data['added'] = True
                except MyListModel.DoesNotExist:
                    data['added'] = False

        return data