from rest_framework import viewsets
from ..models import TvModel, TvGenreModel, CastModel, KeywordModel
from ..models import MovieTvRecomModel, MovieModel, TvTvRecomModel
from django.db.models import QuerySet, Q
from rest_framework.permissions import  AllowAny
from ..serializers import TvSerializer, GenreTvSerializer, BasicTvSerializer, CastSerializer, KeywordSerializer
from ..serializers import MovieTvSerializer, BasicMovieSerializer, TvTvSerializer
from rest_framework.request import Request, QueryDict
from ..helper import customResponse
from rest_framework.decorators import action
import wordsegment as ws
from django.db.models import Case, When
from ..models import UserModel, TvListModel, TvRatingModel
from ..serializers import TvListSerializer, TvRatingSerializer


class TvViewSet(viewsets.ModelViewSet):
    queryset: QuerySet = TvModel.objects.all()
    permission_classes = [AllowAny]
    serializer_class = TvSerializer


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

        # if qp.get('order_by') is not None:
        #     order_by = qp.get('order_by')
        #     self.queryset = self.queryset.order_by(order_by)

        serializer = BasicTvSerializer(self.queryset, many=True)
        return customResponse(True, serializer.data)

    def retrieve(self, request, *args, **kwargs):

        instance: TvModel = self.get_object()
        print(instance.id)
        serializer = self.get_serializer(instance)


        genres = serializer.data['genres']
        genre_qs = TvGenreModel.objects.filter(pk__in=genres)
        genre_serializer = GenreTvSerializer(genre_qs, many=True)

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

    # @action(detail=False, methods=['GET'])
    # def top_tv(self, request: Request, pk=None):
    #     qp: QueryDict = request.query_params
    #
    #     if qp.get('limit') is not None:
    #         limit = int(qp.get('limit'))
    #         # limit = 10
    #         self.queryset = self.queryset.order_by('-popularity')[0:limit]
    #         serializer = TvSerializer(self.queryset, many=True)
    #         ids = []
    #         for i in serializer.data:
    #             ids.append(i['id'])
    #         data = {
    #             'ids': ids,
    #             "title": "Top Movies"
    #         }
    #         return customResponse(True, data)
    #     else:
    #         return customResponse(True, {"error": "limit not provided"})


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
    def top_tv(self, request: Request, pk=None):
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

            qs: QuerySet = TvGenreModel.objects.get(pk=genre)
            genre_serializer = GenreTvSerializer(qs, many=False)
            data = {
                'list_headere': genre_serializer.data['name']
            }
        self.queryset = self.queryset[0:limit]
        serializer = BasicTvSerializer(self.queryset, many=True)

        data.update(
            {
                "genre_bool": genre_bool,
                "result": serializer.data,
                "media_type": 1,
            }
        )
        print(data)
        return customResponse(True, data)
        # else:
        #     return customResponse(True, {"error": "limit not provided"})

    @action(detail=False, methods=['GET'])
    def recommendations(self, request: Request, pk=None):
        qp: QueryDict = request.query_params
        tv_id = qp.get('tv_id')
        print(tv_id)
        tv_recom: QuerySet = TvTvRecomModel.objects.filter(tv_id1__exact=tv_id).order_by('-score')
        serializer = TvTvSerializer(tv_recom, many=True)
        ids = []
        for row in serializer.data:
            print(str(row))
            ids.append(row['tv_id2'])
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
        tvs: QuerySet = TvModel.objects.filter(pk__in=ids).order_by(preserved)

        serializer_tv = BasicTvSerializer(tvs, many=True)


        movie_recom: QuerySet = MovieTvRecomModel.objects.filter(tv_id__exact=tv_id).order_by('-score')
        serializer = MovieTvSerializer(movie_recom, many=True)
        ids = []
        for row in serializer.data:
            ids.append(row['movie_id'])
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
        movies: QuerySet = MovieModel.objects.filter(pk__in=ids).order_by(preserved)
        serializer_movie = BasicMovieSerializer(movies, many=True)

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

    @action(detail=True, methods=['POST'])
    def like(self, request: Request, *args, **kwargs):
        pk = kwargs['pk']
        data = request.data
        user: UserModel = UserModel.objects.get(pk=data['user_id'])
        print(user.email)
        query_pk = Q(tv__exact=pk)
        query_user = Q(user__exact=user)
        try:
            ratings: TvRatingModel = TvRatingModel.objects.get(query_pk & query_user)
            ratings.rating = 5
            ratings.save()
        except:
            print("does not exist")
            new_rating: TvRatingModel = TvRatingModel(user=user, tv=pk, rating=5)
            new_rating.save()
        ratings: TvRatingModel = TvRatingModel.objects.get(query_pk & query_user)
        return customResponse(True, TvRatingSerializer(ratings, many=False).data)

    @action(detail=True, methods=['POST'])
    def dislike(self, request: Request, *args, **kwargs):
        pk = kwargs['pk']
        data = request.data
        user: UserModel = UserModel.objects.get(pk=data['user_id'])
        print(user.email)
        query_pk = Q(tv__exact=pk)
        query_user = Q(user__exact=user)
        try:
            ratings: TvRatingModel = TvRatingModel.objects.get(query_pk & query_user)
            ratings.rating = 1
            ratings.save()
        except:
            print("does not exist")
            new_rating: TvRatingModel = TvRatingModel(user=user, tv=pk, rating=1)
            new_rating.save()
        ratings: TvRatingModel = TvRatingModel.objects.get(query_pk & query_user)
        return customResponse(True, TvRatingSerializer(ratings, many=False).data)

    @action(detail=True, methods=['POST'])
    def toggle_watchlist(self, request: Request, *args, **kwargs):
        pk = kwargs['pk']
        data = request.data
        user: UserModel = UserModel.objects.get(pk=data['user_id'])
        query_pk = Q(tv__exact=pk)
        query_user = Q(user__exact=user)
        try:
            print("found")
            list_object: TvListModel = TvListModel.objects.get(query_pk & query_user)
            list_object.delete()
            return customResponse(True)
        except TvListModel.DoesNotExist:
            list_object: TvListModel = TvListModel(user=user, tv=pk)
            list_object.save()
            return customResponse(True, TvListSerializer(list_object, many=False).data)
        except Exception as e:
            return customResponse(True, {"error": str(e)})