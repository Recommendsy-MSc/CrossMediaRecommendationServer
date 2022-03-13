from rest_framework import viewsets
from ..models import MovieListModel, TvListModel
from ..serializers import MovieListSerializer, TvListSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from ..helper import customResponse
from rest_framework.decorators import action
from rest_framework.request import Request, QueryDict

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
