from rest_framework import viewsets
from ..models import MovieModel, KeywordModel, CastModel, MovieTvRecomModel, MovieMovieRecomModel
from django.db.models import QuerySet
from rest_framework.permissions import  AllowAny
from ..serializers import MovieSerializer, MovieTvSerializer, BasicTvSerializer
from rest_framework.request import Request, QueryDict
from ..helper import customResponse
from rest_framework.decorators import action
from ..serializers import BasicMovieSerializer, GenreSerializer, KeywordSerializer, CastSerializer
from ..serializers import MovieMovieSerializer
from ..models import GenreModel, TvModel
import wordsegment as ws
from django.db.models import Q
from django.db.models import Case, When


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
        print(spaced)
        sent = ''
        for w in spaced:
            if spaced[0] == w:
                sent = sent + w
            else:
                sent = sent + ' ' + w
        print(sent)
        self.queryset = self.queryset.filter(Q(title__icontains=sent) | Q(title__icontains=string))

        if qp.get('order_by') is not None:
            order_by = qp.get('order_by')
            self.queryset = self.queryset.order_by(order_by)

        serializer = BasicMovieSerializer(self.queryset, many=True)
        return customResponse(True, serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance: MovieModel = self.get_object()
        # print(instance.id)
        serializer = self.get_serializer(instance)

        genres = serializer.data['genres']
        genre_qs = GenreModel.objects.filter(pk__in=genres)
        genre_serializer = GenreSerializer(genre_qs, many=True)

        cast_members = serializer.data['cast_members']
        cast_qs = CastModel.objects.filter(pk__in=cast_members)
        cast_serializer = CastSerializer(cast_qs, many=True)

        keywords = serializer.data['keywords']
        keyword_qs = KeywordModel.objects.filter(pk__in=keywords)
        keyword_serializer = KeywordSerializer(keyword_qs, many=True)

        response = serializer.data
        response.update(
            {
                'genres': genre_serializer.data,
                'cast_members': cast_serializer.data,
                'keywords': keyword_serializer.data,
            }
        )

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
            self.queryset = self.queryset.filter(genres__contains=[genre]).order_by('-popularity')

            qs: QuerySet = GenreModel.objects.get(pk=genre)
            genre_serializer = GenreSerializer(qs, many=False)
            data = {
                'list_header': genre_serializer.data['name'],
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


    @action(detail=False, methods=['GET'])
    def recommendations(self, request: Request, pk=None):
        qp: QueryDict = request.query_params
        movie_id = qp.get('movie_id')
        print(movie_id)
        movie_recom: QuerySet = MovieMovieRecomModel.objects.filter(movie_id1__exact=movie_id).order_by('-score')
        serializer = MovieMovieSerializer(movie_recom, many=True)
        ids = []
        for row in serializer.data:
            ids.append(row['movie_id2'])
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
        movies: QuerySet = MovieModel.objects.filter(pk__in=ids).order_by(preserved)


        serializer_movie = BasicMovieSerializer(movies, many=True)

        tv_recom: QuerySet = MovieTvRecomModel.objects.filter(movie_id__exact=movie_id).order_by('-score')
        serializer = MovieTvSerializer(tv_recom, many=True)
        ids = []
        print(serializer.data)
        for row in serializer.data:
            ids.append(row['tv_id'])
            print(row['tv_id'])
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
        tvs: QuerySet = TvModel.objects.filter(pk__in=ids).order_by(preserved)
        serializer_tv = BasicTvSerializer(tvs, many=True)

        result = {
            'movies': {
                "data": {
                    'list_header': "Movie Recommendations",
                    'result': serializer_movie.data
                }
            },
            'tv': {
                "data": {
                    'list_header': "Tv Recommendations",
                    'result': serializer_tv.data
                }
            }
        }
        return customResponse(True, result)


