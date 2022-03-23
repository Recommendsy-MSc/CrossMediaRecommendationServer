from rest_framework import viewsets
from ..models import BookModel
from django.db.models import QuerySet, Q
from rest_framework.permissions import  AllowAny
from ..serializers import BookSerializer, BookRatingSerializer
from rest_framework.response import Response
from ..models import BookRecpModel, UserModel, BookRatingModel
from ..helper import customResponse
from rest_framework.decorators import action
from rest_framework.request import Request


class BookViewSet(viewsets.ModelViewSet):
    queryset: QuerySet = BookModel.objects.all()
    permission_classes = [AllowAny]
    serializer_class = BookSerializer

    def list(self, request, *args, **kwargs):
        return customResponse(False, {"error": "Not Allowed"})

    def retrieve(self, request, *args, **kwargs):
        instance: BookModel = self.get_object()
        return customResponse(True, BookSerializer(instance, many=False, context={'request': request}).data)

    @action(detail=True, methods=['POST'])
    def like(self, request: Request, *args, **kwargs):
        pk = kwargs['pk']
        data = request.data
        user: UserModel = UserModel.objects.get(pk=data['user_id'])
        query_pk = Q(book__exact=pk)
        query_user = Q(user__exact=user)
        try:
            ratings: BookRatingModel = BookRatingModel.objects.get(query_pk & query_user)
            ratings.rating = 5
            ratings.save()
        except:
            new_rating: BookRatingModel = BookRatingModel(user=user, book=pk, rating=5)
            new_rating.save()

        # calculateCosineSim.delay(data['user_id'])

        ratings: BookRatingModel =BookRatingModel.objects.get(query_pk & query_user)
        return customResponse(True, BookRatingSerializer(ratings, many=False).data)

    @action(detail=True, methods=['POST'])
    def dislike(self, request: Request, *args, **kwargs):
        pk = kwargs['pk']
        data = request.data
        user: UserModel = UserModel.objects.get(pk=data['user_id'])
        query_pk = Q(book__exact=pk)
        query_user = Q(user__exact=user)
        try:
            ratings: BookRatingModel = BookRatingModel.objects.get(query_pk & query_user)
            ratings.rating = 1
            ratings.save()
        except:
            new_rating: BookRatingModel = BookRatingModel(user=user, movie=pk, rating=1)
            new_rating.save()

        # calculateCosineSim.delay(data['user_id'])

        ratings: BookRatingModel = BookRatingModel.objects.get(query_pk & query_user)
        return customResponse(True, BookRatingSerializer(ratings, many=False).data)
