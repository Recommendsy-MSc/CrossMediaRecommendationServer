from rest_framework import viewsets
from ..models import MovieListModel, TvListModel, MyListModel, MovieModel, TvModel, BookModel
from ..serializers import MovieListSerializer, TvListSerializer, MyListSerializer, BasicMovieSerializer, BasicTvSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from ..helper import customResponse
from rest_framework.decorators import action
from rest_framework.request import Request, QueryDict
from django.db.models import Q
from ..serializers import BasicBookSerializer


class MyListView(viewsets.ModelViewSet):
    queryset = MyListModel.objects.all()
    serializer_class = MyListSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if not request.user is None:
            try:
                query_user = Q(user_id__exact=request.data['user'],)
                query_title = Q(title__exact=request.data['title'])
                query_type = Q(title_type__exact=request.data['title_type'])
                existing: MyListModel = MyListModel.objects.get(query_type & query_title & query_user)
                existing.delete()
                return customResponse(True, {"error": "already exists, removed"})
            except MyListModel.DoesNotExist:
                return customResponse(True,  super(MyListView, self).create(request, *args, **kwargs).data)
            except Exception as e:
                return customResponse(False, {"error": str(e)})
        else:
            return customResponse(False, {"error": "Authentication not provided"})


    def list(self, request: Request, *args, **kwargs):
        if not request.user is None:
            self.queryset = self.queryset.filter(user__exact=request.user).order_by('-created_date')
            data = []
            for row in self.queryset:

                if row.title_type == 0:
                    movie = MovieModel.objects.get(pk__exact=row.title)
                    data.append(BasicMovieSerializer(movie, many=False, context={'request': request}).data)
                elif row.title_type == 1:
                    tv = TvModel.objects.get(pk__exact=row.title)
                    data.append(BasicTvSerializer(tv, many=False, context={'request': request}).data)
                elif row.title_type == 3:
                    book = BookModel.objects.get(pk__exact=row.title)
                    data.append(BasicBookSerializer(book, many=False, context={'request': request}).data)
            return customResponse(True, data)
        else:
            return customResponse(False, {"error": "Authentication not provided"})


class MovieListView(viewsets.ModelViewSet):
    queryset = MovieListModel.objects.all()
    serializer_class = MovieListSerializer
    permission_classes = [AllowAny]


    @action(detail=False, methods=['GET'])
    def get_list_for_user(self, request: Request, *args, **kwargs):
        qp: QueryDict = request.query_params
        if qp.get('user') != None:
            self.queryset = self.queryset.filter(user__exact=qp.get('user'))
            serializer = self.serializer_class(self.queryset, many=True)
            print(serializer.data)
            return customResponse(True, serializer.data)
        else:
            return customResponse(False, {"error": "User not provided"})


    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return customResponse(True, serializer.data)

    @action(detail=False, methods=['POST'])
    def remove(self, request: Request, *args, **kwargs):
        try:
            data = request.data
            print(data)
            self.queryset = self.queryset.filter(user__exact=data['user'], movie__exact=data['movie']).delete()
            return customResponse(True,)

        except Exception as e:
            return customResponse(False, {"error": str(e)})


class TvListView(viewsets.ModelViewSet):
    queryset = TvListModel.objects.all()
    serializer_class = TvListSerializer
    permission_classes = [AllowAny]


    @action(detail=False, methods=['GET'])
    def get_list_for_user(self, request: Request, *args, **kwargs):
        qp: QueryDict = request.query_params
        if qp.get('user') != None:
            self.queryset = self.queryset.filter(user__exact=qp.get('user'))
            serializer = self.serializer_class(self.queryset, many=True)
            print(serializer.data)
            return customResponse(True, serializer.data)
        else:
            return customResponse(False, {"error": "User not provided"})


    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return customResponse(True, serializer.data)

    @action(detail=False, methods=['POST'])
    def remove(self, request: Request, *args, **kwargs):
        try:
            data = request.data
            print(data)
            self.queryset = self.queryset.filter(user__exact=data['user'], tv__exact=data['tv']).delete()
            return customResponse(True, )

        except Exception as e:
            return customResponse(False, {"error": str(e)})
