from rest_framework import viewsets
from ..models import MovieMovieRecomModel, MovieTvRecomModel, TvTvRecomModel
from ..serializers import MovieMovieSerializer, MovieTvSerializer, TvTvSerializer
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from django.db.models import Q
from ..helper import customResponse

class MovieMovieViewSet(viewsets.ModelViewSet):
    serializer_class = MovieMovieSerializer
    queryset = MovieMovieRecomModel.objects.all()
    permission_classes = [AllowAny]

    @action(methods=['POST'], detail=False)
    def toggle_validation(self, request, *args, **kwargs):
        data = request.data
        query1 = Q(movie_id1__exact=data['movie1'])
        query2 = Q(movie_id2__exact=data['movie2'])
        try:
            model: MovieMovieRecomModel = self.queryset.get(query1 & query2)
            model.valid = not model.valid
            model.save()
            serializer = self.serializer_class(model, many=False)
            return customResponse(True, serializer.data)
        except Exception as e:
            return customResponse(False, {"error": str(e)})


class MovieTvViewSet(viewsets.ModelViewSet):
    serializer_class = MovieTvSerializer
    queryset = MovieTvRecomModel.objects.all()
    permission_classes = [AllowAny]

    @action(methods=['POST'], detail=False)
    def toggle_validation(self, request, *args, **kwargs):
        data = request.data
        query1 = Q(movie_id__exact=data['movie'])
        query2 = Q(tv_id__exact=data['tv'])
        try:
            model: MovieTvRecomModel = self.queryset.get(query1 & query2)
            model.valid = not model.valid
            model.save()
            serializer = self.serializer_class(model, many=False)
            return customResponse(True, serializer.data)
        except Exception as e:
            return customResponse(False, {"error": str(e)})


class TvTvViewSet(viewsets.ModelViewSet):
    serializer_class = TvTvSerializer
    queryset = TvTvRecomModel.objects.all()
    permission_classes = [AllowAny]

    @action(methods=['POST'], detail=False)
    def toggle_validation(self, request, *args, **kwargs):
        data = request.data
        query1 = Q(tv_id1__exact=data['tv1'])
        query2 = Q(tv_id2__exact=data['tv2'])
        try:
            model: TvTvRecomModel = self.queryset.get(query1 & query2)
            model.valid = not model.valid
            model.save()
            serializer = self.serializer_class(model, many=False)
            return customResponse(True, serializer.data)
        except Exception as e:
            return customResponse(False, {"error": str(e)})