from rest_framework import viewsets
from ..models import MovieRatingModel
from django.db.models import QuerySet
from rest_framework.permissions import  AllowAny
from ..serializers import MovieRatingSerializer
from ..helper import customResponse

class MovieRatingViewSet(viewsets.ModelViewSet):
    queryset: QuerySet = MovieRatingModel.objects.all()
    permission_classes = [AllowAny]
    serializer_class = MovieRatingSerializer


    def create(self, request, *args, **kwargs):
        data = request.data
        print(data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return customResponse(True, serializer.data)

    def retrieve(self, request, *args, **kwargs):
        print(request.data)
        print(self.kwargs['pk'])
        movie_id = self.kwargs['pk']

        try:
            self.queryset = self.queryset.filter(movie__exact=movie_id)

            if self.queryset:
                serializer = MovieRatingSerializer(self.queryset, many=True)
                print(serializer.data)
                sum = 0
                for i in serializer.data:
                    sum = sum + i['rating']
                avg = round(sum / len(serializer.data), 2)
                percent = round(avg*20, 2)

                return customResponse(True, {"avg": avg, "percent": percent})
            else:
                return customResponse(False, {'error': "Movie Not Found"})
        except Exception as e:
            return customResponse(False, {'error': e})


