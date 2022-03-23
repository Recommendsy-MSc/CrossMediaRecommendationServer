from rest_framework import viewsets
from ..models import UserModel, GenreModel, TvGenreModel
from django.db.models import QuerySet, Q
from rest_framework.permissions import AllowAny, IsAuthenticated
from ..serializers import UserSerializer, GenreSerializer, GenreTvSerializer
from ..helper import customResponse
from rest_framework.request import Request, QueryDict
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from ..models import SimilarityModel, TvRatingModel, MovieRatingModel, MovieModel, TvModel
from ..serializers import BasicMovieSerializer, BasicTvSerializer
from django.db.models import Case, When
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate


class UserViewSet(viewsets.ModelViewSet):
    queryset: QuerySet = UserModel.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    # Configures Permissions for Individual View Actions

    def get_permissions(self):
        print(self.action)
        if self.action == 'create' or self.action == 'exists' or self.action == 'login':
            self.permission_classes = [AllowAny, ]
        else:
            self.permission_classes = [IsAuthenticated, ]

        return super().get_permissions()

    @action(methods=['POST'], detail=False)
    def login(self, request: Request):
        data = request.data
        user = authenticate(email=data['email'], password=data['password'])
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            serializer_data = UserSerializer(user, many=False).data
            serializer_data.pop('password')
            resp = {
                "user": serializer_data,
                "token": token.key
            }
            return customResponse(True, resp)
        else:
            return customResponse(False)


    @action(detail=False, methods=['POST', 'GET'], )
    def exists(self, request: Request, pk=None):
        data = request.data
        print(str(data))
        email = data.get('email')
        print(email)
        try:
            user: UserModel = UserModel.objects.filter(email__exact=email).get()
            serializer = UserSerializer(user, many=False)
            resp = serializer.data
            resp.pop('password')
            token, created = Token.objects.get_or_create(user=user)
            print(token.key)
            resp = {
                'token': token.key,
                'user': resp,
            }
            return customResponse(True, resp)
        except Exception as e:
            print(e)
            return customResponse(False, {"error": str(e)})

    def retrieve(self, request, *args, **kwargs):
        instance: UserModel = self.get_object()
        serializer = self.get_serializer(instance)
        resp = serializer.data
        resp.pop('password')
        return customResponse(True, resp)


    def create(self, request, *args, **kwargs):
        # return customResponse(False, {"error": "Method Not Allowed"})
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            user = UserModel.objects.get_by_natural_key(serializer.validated_data.get('email'))
            token, created = Token.objects.get_or_create(user=user)
            data = serializer.data
            data.pop('password')
            resp = {
                'token': token.key,
                'user': data
            }
            return customResponse(True, resp)
        except:
            return customResponse(False,)


    @action(methods=['GET'], detail=True)
    def recommend_movies(self, request: Request, *args, **kwargs):
        limit = 20
        page = 1
        qp: QueryDict = request.query_params
        if not qp.get('limit') is None:
            limit = int(qp.get('limit'))
        if not qp.get('page') is None:
            page = int(qp.get('page'))
        query_similarity_threshold = Q(similarity__gt=0.6)
        query_user1 = Q(user1_id__exact=kwargs['pk'])
        query_user2 = Q(user2_id__exact=kwargs['pk'])
        s_model: QuerySet = (SimilarityModel.objects.filter(query_user1 & query_similarity_threshold)).union(SimilarityModel.objects.filter(query_user2 & query_similarity_threshold)).order_by('-similarity')
        movies_rated = list(MovieRatingModel.objects.filter(user_id__exact=kwargs['pk']).values_list('movie', flat=True))

        like_users_model = []
        print(kwargs['pk'])
        for row in s_model:
            print(row.similarity)
            if row.user1_id == int(kwargs['pk']):
                print("U2")
                like_users_model.append(row.user2)
            else:
                print("U1")
                like_users_model.append(row.user1)

        recommended_movie_ids = []
        query_liked = Q(rating__exact=5)
        query_exclued_rated = Q(movie__in=movies_rated)
        for cur_user in like_users_model:
            print(cur_user.id)
            query_user = Q(user__exact=cur_user)
            user_liked_movies = list(MovieRatingModel.objects.filter(query_user & query_liked).exclude(query_exclued_rated).values_list('movie', flat=True))
            print(user_liked_movies)
            for id in user_liked_movies:
                if not id in recommended_movie_ids:
                    recommended_movie_ids.append(id)

        print(recommended_movie_ids)

        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(recommended_movie_ids)])
        if not qp.get('genre') is None:
            query_genre = Q(genres__contains=[qp.get('genre')])
            query_ids = Q(pk__in=recommended_movie_ids)
            recommended_movies = MovieModel.objects.filter(query_ids & query_genre).order_by(preserved)

            if len(recommended_movies) > limit:
                recommended_movies = recommended_movies[(page-1)*limit:limit*page]
                print("new length")
                print(len(recommended_movies))
            serializer = BasicMovieSerializer(recommended_movies, many=True, context={'request': request})
            qs: QuerySet = GenreModel.objects.get(pk=qp.get('genre'))
            genre_serializer = GenreSerializer(qs, many=False)
            resp = {
                'list_header': genre_serializer.data['name'],
                'result': serializer.data,
                'page': page,
                'limit': limit,
                'count': len(serializer.data)
            }
            return customResponse(True, resp)
        else:
            recommended_movies = MovieModel.objects.filter(pk__in=recommended_movie_ids).order_by(preserved)

            if len(recommended_movies) > limit:
                recommended_movies = recommended_movies[(page-1)*limit:limit*page]
                print("new length")
                print(len(recommended_movies))

            serializer = BasicMovieSerializer(recommended_movies, many=True, context={'request': request})
            resp = {
                'list_header': "Movies For You",
                'result': serializer.data,
                'page': page,
                'limit': limit,
                'count': len(serializer.data)
            }
            return customResponse(True, resp)

    @action(methods=['GET'], detail=True)
    def recommend_tv(self, request: Request, *args, **kwargs):
        limit = 20
        page = 1
        qp: QueryDict = request.query_params
        if not qp.get('limit') is None:
            limit = int(qp.get('limit'))
        if not qp.get('page') is None:
            page = int(qp.get('page'))
        query_similarity_threshold = Q(similarity__gt=0.6)
        query_user1 = Q(user1_id__exact=kwargs['pk'])
        query_user2 = Q(user2_id__exact=kwargs['pk'])
        s_model: QuerySet = (SimilarityModel.objects.filter(query_user1 & query_similarity_threshold)).union(
            SimilarityModel.objects.filter(query_user2 & query_similarity_threshold)).order_by('-similarity')
        tv_rated = list(
            TvRatingModel.objects.filter(user_id__exact=kwargs['pk']).values_list('tv', flat=True))

        like_users_model = []
        for row in s_model:
            if row.user1_id == int(kwargs['pk']):
                like_users_model.append(row.user2)
            else:
                like_users_model.append(row.user1)

        print(like_users_model)
        recommended_tv_ids = []
        query_liked = Q(rating__exact=5)
        query_exclued_rated = Q(tv__in=tv_rated)
        for cur_user in like_users_model:
            query_user = Q(user__exact=cur_user)
            user_liked_tv = list(
                TvRatingModel.objects.filter(query_user & query_liked).exclude(query_exclued_rated).values_list(
                    'tv', flat=True))
            for id in user_liked_tv:
                if not id in recommended_tv_ids:
                    recommended_tv_ids.append(id)

        print(recommended_tv_ids)

        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(recommended_tv_ids)])
        if not qp.get('genre') is None:
            query_genre = Q(genres__contains=[qp.get('genre')])
            query_ids = Q(pk__in=recommended_tv_ids)
            recommended_tv = TvModel.objects.filter(query_ids & query_genre).order_by(preserved)

            if len(recommended_tv) > limit:
                recommended_tv = recommended_tv[(page-1)*limit:limit*page]

            serializer = BasicTvSerializer(recommended_tv, many=True, context={'request': request})
            qs: QuerySet = TvGenreModel.objects.get(pk=qp.get('genre'))
            genre_serializer = GenreTvSerializer(qs, many=False)
            resp = {
                'list_header': genre_serializer.data['name'],
                'result': serializer.data,
                'page': page,
                'limit': limit,
                'count': len(serializer.data)
            }
            return customResponse(True, resp)
        else:
            recommended_tv = TvModel.objects.filter(pk__in=recommended_tv_ids).order_by(preserved)
            if len(recommended_tv) > limit:
                recommended_tv = recommended_tv[(page-1)*limit:limit*page]
            serializer = BasicTvSerializer(recommended_tv, many=True, context={'request': request})
            resp = {
                'list_headed': "Shows For You",
                'result': serializer.data,
                'page': page,
                'limit': limit,
                'count': len(serializer.data)
            }
            return customResponse(True, resp)
# custom auth token so that can return desired response

class ObtainAuthTokenViewSet(ObtainAuthToken):
    def get(self, request):
        return Response(
            {
                "hi": "hello"
            }
        )

    def post(self, request, *args, **kwargs):
        print(request)
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(
                {
                    "success": "false",
                    "error": "Invalid Credentials",
                },
                status=HTTP_401_UNAUTHORIZED
            )

        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        user = UserModel.objects.get(id=token.user_id)
        resp = UserSerializer(user).data
        resp.pop('password')
        data = {'auth_token': token.key, 'user': resp}
        return customResponse(True, data)



class CreateExistingToken(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        for user in UserModel.objects.all():
            Token.objects.get_or_create(user=user)

        return Response(
            {
                "success": "true"
            }
        )
