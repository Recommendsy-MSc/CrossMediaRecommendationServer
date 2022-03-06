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

class MovieViewSet(viewsets.ModelViewSet):
    queryset: QuerySet = MovieModel.objects.all()
    permission_classes = [AllowAny]
    serializer_class = MovieSerializer

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

    # @action(detail=True)
    # def basic(self, request: Request, pk=None):
    #     movie_id = pk
    #     mov: MovieModel = MovieModel.objects.get(pk=movie_id)
    #     recp: MovieRecpModel = MovieRecpModel.objects.get(pk=movie_id)
    #
    #     fil = {
    #         'movie': mov,
    #         'recp': recp
    #     }
    #
    #     serializer = MovieTileSerializer(fil)
    #     print(serializer.data)
    #
    #     return customResponse(True, serializer.data)


    # currently its based on popularity
    # TODO: Change it to Ratings
    @action(detail=False, methods=['GET'])
    def top_movies(self, request: Request, pk=None):
        qp: QueryDict = request.query_params
        data = {}
        genre_bool = False
        if qp.get('limit') is not None:
            limit = int(qp.get('limit'))
            # limit = 10

            if qp.get('genre') is not None:
                genre_bool = True
                genre = qp.get('genre')
                self.queryset = MovieModel.objects.filter(genres__contains=[genre])

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
        else:
            return customResponse(True, {"error": "limit not provided"})




