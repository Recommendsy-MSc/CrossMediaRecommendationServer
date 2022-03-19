from rest_framework import viewsets
from ..models import MovieModel, TvModel
from rest_framework.permissions import AllowAny
from rest_framework.request import QueryDict, Request
import wordsegment as ws
from ..helper import customResponse
from ..serializers import BasicMovieSerializer, BasicTvSerializer
from django.db.models import Q


class SearchViewSet(viewsets.ModelViewSet):
    movie_queryset = MovieModel.objects.all()
    tv_queryset = TvModel.objects.all()
    permission_classes = [AllowAny, ]
    http_method_names = ['get']

    def retrieve(self, request, *args, **kwargs):
        return customResponse(False, {"error": "Not Allowed"})

    def list(self, request: Request, *args, **kwargs):
        qp: QueryDict = request.query_params

        if qp.get('q') is not None:
            string = qp.get('q')
            ws.load()
            spaced = ws.segment(string)
            sent = ''
            for w in spaced:
                if spaced[0] == w:
                    sent = sent + w
                else:
                    sent = sent + ' ' + w
            self.movie_queryset = self.movie_queryset.filter(Q(title__icontains=sent) | Q(title__icontains=string))
            self.tv_queryset = self.tv_queryset.filter(Q(title__icontains=sent) | Q(title__icontains=string))

            if qp.get('order_by') is not None:
                order_by = qp.get('order_by')
                self.movie_queryset = self.movie_queryset.order_by(order_by)

            movie_serializer = BasicMovieSerializer(self.movie_queryset, many=True, context={'request': request})
            tv_serializer = BasicTvSerializer(self.tv_queryset, many=True, context={'request': request})
            print(len(tv_serializer.data))
            data = {
                'movies': {
                    'count': len(movie_serializer.data),
                    'data': {
                        'result': movie_serializer.data,
                        'list_header': 'Movies'
                    },
                    
                },
                'tv': {
                    'count': len(tv_serializer.data),
                    'data': {
                        'result': tv_serializer.data,
                        'list_header': 'Tv Shows'
                    },

                }
            }

            return customResponse(True, data)
        else:
            return customResponse(False, {"error": "Search String required"})

