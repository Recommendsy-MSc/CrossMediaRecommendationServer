from rest_framework import viewsets
from ..models import MovieModel, MovieRatingModel
from django.db.models import QuerySet
from rest_framework.permissions import  AllowAny
from ..serializers import MovieSerializer, MovieRecpSerializer, MovieRatingSerializer
from rest_framework.response import Response
from rest_framework.request import Request, QueryDict
from ..models import MovieRecpModel
from ..helper import customResponse
from rest_framework.decorators import action
from ..serializers import BasicMovieSerializer, GenreSerializer
from ..models import GenreModel
import wordsegment as ws
from django.db.models import Q

class MovieViewSet(viewsets.ModelViewSet):
    queryset: QuerySet = MovieModel.objects.all()
    permission_classes = [AllowAny]
    serializer_class = MovieSerializer

    @action(detail=False, methods=['GET'])
    def search(self, request, *args, **kwargs):
        qp: QueryDict = request.query_params
        string = qp['q']
        ws.load()
        spaced = ws.segment(string)
        sent = ''
        for w in spaced:
            if spaced[0] == w:
                sent = sent + w
            else:
                sent = sent + ' ' + w
        self.queryset = self.queryset.filter(title__icontains=sent)

        if qp.get('order_by') is not None:
            order_by = qp.get('order_by')
            self.queryset = self.queryset.order_by(order_by)

        serializer = BasicMovieSerializer(self.queryset, many=True)
        return customResponse(True, serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance: MovieModel = self.get_object()
        # print(instance.id)
        serializer = self.get_serializer(instance)
        response = serializer.data
        response.update({'media_type': '0'})
        return customResponse(True, response)

    def list(self, request, *args, **kwargs):
        return customResponse(
            True,
            {
                "success": False,
                "error": "Long Request"
            }
      )

    # currently its based on popularity
    # TODO: Change it to Ratings
    @action(detail=False, methods=['GET'])
    def top_movies(self, request: Request, pk=None):
        qp: QueryDict = request.query_params
        data = {}
        genre_bool = False
        limit = 20
        if qp.get('limit') is not None:
            limit = int(qp.get('limit'))
            # limit = 10

        if qp.get('genre') is not None:
            genre_bool = True
            genre = qp.get('genre')
            self.queryset = self.queryset.filter(genres__contains=[genre])

            qs: QuerySet = GenreModel.objects.get(pk=genre)
            genre_serializer = GenreSerializer(qs, many=False)
            data = {
                'genre_title': genre_serializer.data['name']
            }
        self.queryset = self.queryset[0:limit]
        serializer = BasicMovieSerializer(self.queryset, many=True)

        data.update(
            {
                "genre_bool": genre_bool,
                "result": serializer.data,
                "media_type": 0,
            }
        )
        print(data)
        return customResponse(True, data)
        # else:
        #     return customResponse(True, {"error": "limit not provided"})




