from rest_framework import viewsets
from ..models import TvModel, TvGenreModel
from django.db.models import QuerySet
from rest_framework.permissions import  AllowAny
from ..serializers import TvSerializer, GenreTvSerializer, BasicTvSerializer
from rest_framework.request import Request, QueryDict
from ..models import TvRecpModel
from ..helper import customResponse
from rest_framework.decorators import action



class TvViewSet(viewsets.ModelViewSet):
    queryset: QuerySet = TvModel.objects.all()
    permission_classes = [AllowAny]
    serializer_class = TvSerializer

    def retrieve(self, request, *args, **kwargs):
        instance: TvModel = self.get_object()
        print(instance.id)
        serializer = self.get_serializer(instance)
        response = serializer.data
        response.update({'media_type': '1'})
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
                'genre_title': genre_serializer.data['name']
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