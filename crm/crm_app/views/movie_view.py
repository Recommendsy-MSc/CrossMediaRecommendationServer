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
from ..models import MovieRatingModel
from ..models import UserModel
from ..serializers import MovieRatingSerializer, MovieListSerializer
from ..models import MovieListModel, InaccurateDataModel, InaccurateRecomModel, BrokenLinkModel
from ..serializers import InaccurateDataSerializer, InaccurateRecomSerializer, BrokenLinkSerializer
from ..task import calculate_user_su, calculate_similarity


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
        if qp.get('valid') is not None:
            movie_recom = movie_recom.filter(valid__exact=qp.get('valid'))
        serializer = MovieMovieSerializer(movie_recom, many=True)
        ids = []
        for row in serializer.data:
            ids.append(row['movie_id2'])
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
        movies: QuerySet = MovieModel.objects.filter(pk__in=ids).order_by(preserved)

        serializer_movie = BasicMovieSerializer(movies, many=True)


        tv_recom: QuerySet = MovieTvRecomModel.objects.filter(movie_id__exact=movie_id).order_by('-score')
        if qp.get('valid') is not None:
            tv_recom = tv_recom.filter(valid__exact=qp.get('valid'))

        serializer = MovieTvSerializer(tv_recom, many=True)
        ids = []
        for row in serializer.data:
            ids.append(row['tv_id'])

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


    @action(detail=True, methods=['POST'])
    def like(self, request: Request, *args, **kwargs):
        pk = kwargs['pk']
        data = request.data
        user: UserModel = UserModel.objects.get(pk=data['user_id'])
        print(user.email)
        query_pk = Q(movie__exact=pk)
        query_user = Q(user__exact=user)
        try:
            ratings: MovieRatingModel = MovieRatingModel.objects.get(query_pk & query_user)
            ratings.rating = 5
            ratings.save()
        except:
            print("does not exist")
            new_rating: MovieRatingModel = MovieRatingModel(user=user, movie=pk, rating=5)
            new_rating.save()

        calculate_user_su.delay(data['user_id'])
        calculate_similarity.delay(data['user_id'])
        ratings: MovieRatingModel = MovieRatingModel.objects.get(query_pk & query_user)
        return customResponse(True, MovieRatingSerializer(ratings, many=False).data)

    @action(detail=True, methods=['POST'])
    def dislike(self, request: Request, *args, **kwargs):
        pk = kwargs['pk']
        data = request.data
        user: UserModel = UserModel.objects.get(pk=data['user_id'])
        print(user.email)
        query_pk = Q(movie__exact=pk)
        query_user = Q(user__exact=user)
        try:
            ratings: MovieRatingModel = MovieRatingModel.objects.get(query_pk & query_user)
            ratings.rating = 1
            ratings.save()
        except:
            print("does not exist")
            new_rating: MovieRatingModel = MovieRatingModel(user=user, movie=pk, rating=1)
            new_rating.save()

        calculate_user_su.delay(data['user_id'])
        calculate_similarity.delay(data['user_id'])

        ratings: MovieRatingModel = MovieRatingModel.objects.get(query_pk & query_user)
        return customResponse(True, MovieRatingSerializer(ratings, many=False).data)

    @action(detail=True, methods=['POST'])
    def toggle_watchlist(self,  request: Request, *args, **kwargs):
        pk = kwargs['pk']
        data = request.data
        user: UserModel = UserModel.objects.get(pk=data['user_id'])
        query_pk = Q(movie__exact=pk)
        query_user = Q(user__exact=user)
        try:
            print("found")
            list_object: MovieListModel = MovieListModel.objects.get(query_pk & query_user)
            list_object.delete()
            return customResponse(True)
        except MovieListModel.DoesNotExist:
            list_object: MovieListModel = MovieListModel(user=user, movie=pk)
            list_object.save()
            return customResponse(True, MovieListSerializer(list_object, many=False).data)
        except Exception as e:
            return customResponse(True, {"error": str(e)})


    @action(detail=True, methods=['POST'])
    def inaccurate_data(self, request: Request, *args, **kwargs):
        pk = kwargs['pk']
        data = request.data
        user: UserModel = UserModel.objects.get(pk=data['user_id'])
        movie: MovieModel = MovieModel.objects.get(pk=pk)
        instance: InaccurateDataModel = InaccurateDataModel(
            user=user,
            title=pk,
            note=data['note'],
            type=0,
        )
        instance.save()
        return customResponse(True, InaccurateDataSerializer(instance, many=False).data)


    @action(detail=True, methods=['GET'])
    def broken_link(self, request: Request, *args, **kwargs):
        pk = kwargs['pk']
        query_title = Q(title__exact=pk)

        try:
            instance: BrokenLinkModel = BrokenLinkModel.objects.get(query_title)
            instance.count = instance.count + 1
            instance.save()
            return customResponse(True, BrokenLinkSerializer(instance, many=False).data)
        except BrokenLinkModel.DoesNotExist:
            movie: MovieModel = MovieModel.objects.get(pk=pk)
            instance: BrokenLinkModel = BrokenLinkModel(title=pk,)
            instance.save()
            return customResponse(True, BrokenLinkSerializer(instance, many=False).data)
        except Exception as e:
            return customResponse(False, {"error": str(e)})


    @action(detail=True, methods=['POST'])
    def inaccurate_recom(self, request: Request, *args, **kwargs):
        pk = kwargs['pk']
        data = request.data
        query_title = Q(title__exact=pk)
        query_title2 = Q(recommended_title__exact=data['recommended_title'])
        query_type2 = Q(recommended_type__exact=data['recommended_type'])
        print(data['recommended_type'])
        query_type = Q(type__exact=0)
        try:

            instance: InaccurateRecomModel = InaccurateRecomModel.objects.get(
                query_title & query_title2 & query_type & query_type2
            )
            print("found")
            instance.count = instance.count+1
            instance.save()
            return customResponse(True, InaccurateRecomSerializer(instance, many=False).data)
        except InaccurateRecomModel.DoesNotExist:
            movie: MovieModel = MovieModel.objects.get(pk=pk)
            if data['recommended_type'] == 0:
                movie2: MovieModel = MovieModel.objects.get(pk=data['recommended_title'])
                name = movie2.title
            elif data['recommended_type'] == 1:
                tv: TvModel = TvModel.objects.get(pk=data['recommended_title'])
                name = tv.title
            instance: InaccurateRecomModel = InaccurateRecomModel(
                title=pk,
                recommended_title=data['recommended_title'],
                recommended_type=data['recommended_type'],
            )
            instance.save()
            return customResponse(True, InaccurateRecomSerializer(instance, many=False).data)
        except Exception as e:
            return customResponse(False, {"error": str(e)})

    def partial_update(self, request, *args, **kwargs):
        try:
            return customResponse(True, super(MovieViewSet, self).partial_update(request, *args, **kwargs).data)
        except Exception as e:
            print(e)
            return customResponse(False, {"error": str(e)})

