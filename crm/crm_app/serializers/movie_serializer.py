from rest_framework import serializers
from ..models import MovieModel, MovieRecpModel, MovieRatingModel, UserModel
from .rating_serializer import MovieRatingSerializer
from django.db.models import Q
from rest_framework.request import Request


class MovieSerializer(serializers.ModelSerializer):
    title_type = serializers.IntegerField(default=0)
    class Meta:
        model = MovieModel
        fields = '__all__'
        extra_fields = ('title_type', )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request: Request = self.context.get('request')
        if request and hasattr(request, 'user'):
            if not request.user.id is None:
                query_user = Q(user__exact=request.user)
                query_movie = Q(movie__exact=data['id'])
                try:
                    rated: MovieRatingModel = MovieRatingModel.objects.get(query_movie & query_user)
                    data['user_rating'] = rated.rating
                except MovieRatingModel.DoesNotExist:
                    pass
        return data


# class MovieRecpSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = MovieRecpModel
#         fields = '__all__'
#
#     def to_representation(self, instance):
#         data = super().to_representation(instance)
#         request: Request = self.context.get('request')
#         if request and hasattr(request, 'user'):
#             if not request.user.id is None:
#                 query_user = Q(user__exact=request.user)
#                 query_movie = Q(movie__exact=data['id'])
#                 try:
#                     rated: MovieRatingModel = MovieRatingModel.objects.get(query_movie & query_user)
#                     data['user_rating'] = rated.rating
#                 except MovieRatingModel.DoesNotExist:
#                     pass
#         return data


class BasicMovieSerializer(serializers.ModelSerializer):
    title_type = serializers.IntegerField(default=0)
    class Meta:
        model = MovieModel
        fields = ('id', 'title', 'poster_path', 'title_type', )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request: Request = self.context.get('request')
        if request and hasattr(request, 'user'):
            if not request.user.id is None:
                query_user = Q(user__exact=request.user)
                query_movie = Q(movie__exact=data['id'])
                try:

                    rated: MovieRatingModel = MovieRatingModel.objects.get(query_movie & query_user)
                    data['user_rating'] = rated.rating
                except MovieRatingModel.DoesNotExist:
                    pass
        return data


# class BasicMovieSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = MovieModel
#         fields = ('poster_path', )
#
#
# class BasicMovieRecpSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = MovieRecpModel
#         fields = ('title', )
#
#
# class MovieTileSerializer(serializers.ModelSerializer):
#     movie = BasicMovieSerializer()
#     recp = BasicMovieRecpSerializer()
#
#     class Meta:
#         model = BasicMovieModel
#         fields = ('movie', 'recp')


