from rest_framework import viewsets
from rest_framework.request import Request, QueryDict
from ..models import InaccurateDataModel, InaccurateRecomModel, BrokenLinkModel
from ..serializers import InaccurateDataSerializer, InaccurateRecomSerializer, BrokenLinkSerializer
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from ..helper import customResponse
from ..models import MovieModel, TvModel


class InaccurateDataView(viewsets.ModelViewSet):
    queryset = InaccurateDataModel.objects.all()
    permission_classes = [AllowAny]
    serializer_class = InaccurateDataSerializer


    def partial_update(self, request, *args, **kwargs):
        print(request.data)
        try:
            resp = super(InaccurateDataView, self).partial_update(request, *args, **kwargs)
            return customResponse(True, resp.data)
        except Exception as e:
            print(e)
            return customResponse(False, {"error": str(e)})

    @action(detail=False, methods=['GET'])
    def get_latest(self, request: Request, *args, **kwargs):
        qp: QueryDict = request.query_params
        if qp.get('active'):
            self.queryset = self.queryset.filter(active__exact=qp.get('active'))
        self.queryset = self.queryset.order_by('-created_date')
        serializer = self.serializer_class(self.queryset, many=True)
        data = serializer.data
        for row in data:
            print(row['title'])
            if row['type'] == 0:
                movie: MovieModel = MovieModel.objects.get(pk=row['title'])
                row['name'] = movie.title
            elif row['type'] == 1:
                tv: TvModel = TvModel.objects.get(pk=row['title'])
                row['name'] = tv.title

        return customResponse(True, data)


class InaccurateRecomView(viewsets.ModelViewSet):
    queryset = InaccurateRecomModel.objects.all()
    permission_classes = [AllowAny]
    serializer_class = InaccurateRecomSerializer


    def partial_update(self, request, *args, **kwargs):
        print(request.data)
        try:
            resp = super(InaccurateRecomView, self).partial_update(request, *args, **kwargs)
            return customResponse(True, resp.data)
        except Exception as e:
            print(e)
            return customResponse(False, {"error": str(e)})

    def list(self, request: Request, *args, **kwargs):
        qp: QueryDict = request.query_params
        if qp.get('active'):
            self.queryset = self.queryset.filter(active__exact=qp.get('active'))
        self.queryset = self.queryset.order_by('-count', '-created_date')
        data = InaccurateRecomSerializer(self.queryset, many=True).data

        for row in data:
            if row['type'] == 0:
                movie: MovieModel = MovieModel.objects.get(pk=row['title'])
                row['name'] = movie.title
            elif row['type'] == 1:
                tv: TvModel = TvModel.objects.get(pk=row['title'])
                row['name'] = tv.title

            if row['recommended_type'] == 0:
                recom_movie: MovieModel = MovieModel.objects.get(pk=row['recommended_title'])
                row['recommended_name'] = recom_movie.title
            elif row['recommended_type'] == 1:
                recom_tv: TvModel = TvModel.objects.get(pk=row['recommended_title'])
                row['recommended_name'] = recom_tv.title

        return customResponse(True, data)

class BrokenLinkView(viewsets.ModelViewSet):
    queryset = BrokenLinkModel.objects.all()
    permission_classes = [AllowAny]
    serializer_class = BrokenLinkSerializer

    def partial_update(self, request, *args, **kwargs):
        print(request.data)
        try:
            resp = super(BrokenLinkView, self).partial_update(request, *args, **kwargs)
            return customResponse(True, resp.data)
        except Exception as e:
            print(e)
            return customResponse(False, {"error": str(e)})

    def list(self, request: Request, *args, **kwargs):
        qp: QueryDict = request.query_params
        if qp.get('active'):
            self.queryset = self.queryset.filter(active__exact=qp.get('active'))

        self.queryset = self.queryset.order_by('-count', '-created_date')
        data = BrokenLinkSerializer(self.queryset, many=True).data

        for row in data:
            print(row['title'])
            if row['type'] == 0:
                movie: MovieModel = MovieModel.objects.get(pk=row['title'])
                row['name'] = movie.title
            elif row['type'] == 1:
                tv: TvModel = TvModel.objects.get(pk=row['title'])
                row['name'] = tv.title

        return customResponse(True, data)

