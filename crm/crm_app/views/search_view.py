from rest_framework import viewsets
from ..models import MovieModel, TvModel, GenreModel, TvGenreModel
from rest_framework.permissions import AllowAny
from rest_framework.request import QueryDict, Request
import wordsegment as ws
from ..helper import customResponse
from ..serializers import BasicMovieSerializer, BasicTvSerializer, GenreSerializer, GenreTvSerializer
from django.db.models import Q
from rest_framework.decorators import action
from tmdbv3api import TMDb, Movie, Discover, TV
from ..models import GlobalVarModel
import time

tmdb = TMDb()

class SearchViewSet(viewsets.ModelViewSet):
    movie_queryset = MovieModel.objects.all()
    tv_queryset = TvModel.objects.all()
    permission_classes = [AllowAny, ]
    http_method_names = ['get']

    @action(detail=False)
    def tmdb_movie(self, request: Request, *args, **kwargs):
        qp: QueryDict = request.query_params
        if not request.user is None and request.user.is_superuser:
            if not qp.get('q') is None:
                has_movies = list(MovieModel.objects.all().values_list('id', flat=True))

                search_string = qp.get('q')
                tmdb_api: GlobalVarModel = GlobalVarModel.objects.get(name__exact='tmdb_api_key')
                tmdb.api_key = tmdb_api.value
                movie = Movie()

                page = 1
                if not qp.get('page') is None:
                    page = int(qp.get('page'))

                search = movie.search(search_string, page=page)
                results = []
                count = 0

                for res in search:
                    print(type(res.get('id')))
                    if not str(res.get('id')) in has_movies:

                        data = {
                            'id': res.get('id'),
                            'title': res.get('title'),
                            'release_date': res.get('release_date'),
                            'overview': res.get('overview'),
                            'poster_path': res.get('poster_path'),
                            'backdrop_path': res.get('backdrop_path'),
                            'title_type': 0
                        }

                        try:
                            genres = res.get('genre_ids')
                            genre_qs = GenreModel.objects.filter(pk__in=genres)
                            genre_serializer = GenreSerializer(genre_qs, many=True)
                            data['genres'] = genre_serializer.data
                        except:
                            data['genres'] = []

                        results.append(data)
                        count += 1
                        print("\n")
                data = {
                    'result': results,
                    'count': count
                }
                return customResponse(True, data)
            else:
                return customResponse(False)
        else:
            return customResponse(False, {"error": "Admin Credentials Required"})

    @action(detail=False)
    def tmdb_tv(self, request: Request, *args, **kwargs):
        qp: QueryDict = request.query_params
        if not request.user is None and request.user.is_superuser:
            if not qp.get('q') is None:
                has_tv = list(TvModel.objects.all().values_list('id', flat=True))
                search_string = qp.get('q')
                tmdb_api: GlobalVarModel = GlobalVarModel.objects.get(name__exact='tmdb_api_key')
                tmdb.api_key = tmdb_api.value
                tv = TV()

                page = 1
                if not qp.get('page') is None:
                    page = int(qp.get('page'))

                search = (tv.search(search_string, page=page))
                results = []
                count = 0
                for res in search:
                    if str(res.get('id')) in has_tv:
                        continue
                    data = {
                        'id': res.get('id'),
                        'title': res.get('name'),
                        'first_air_date': res.get('first_air_date'),
                        'overview': res.get('overview'),
                        'poster_path': res.get('poster_path'),
                        'title_type': 1
                    }
                    try:
                        genres = res.get('genre_ids')
                        genre_qs = TvGenreModel.objects.filter(pk__in=genres)
                        genre_serializer = GenreTvSerializer(genre_qs, many=True)
                        data['genres'] = genre_serializer.data
                    except:
                        data['genres'] = []

                    results.append(data)
                    count += 1
                print(len(search))
                data = {
                    'result': results,
                    'count': count
                }
                return customResponse(True, data)
            else:
                return customResponse(False)
        else:
            return customResponse(False, {"error": "Admin Credentials Required"})

    def retrieve(self, request, *args, **kwargs):
        return customResponse(False, {"error": "Not Allowed"})

    def list(self, request: Request, *args, **kwargs):
        qp: QueryDict = request.query_params
        start = time.time()
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
            print("Search Time Taken: " + str(time.time() - start))
            return customResponse(True, data)
        else:
            return customResponse(False, {"error": "Search String required"})

