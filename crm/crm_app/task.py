from celery import shared_task
from .models import MovieRatingModel, TvRatingModel, StandardUnitsModel, SimilarityModel
from .models import UserModel
from math import sqrt, isnan
from django.db.models import Q, QuerySet
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

@shared_task
def random_task():
    print("task run")
    user = UserModel.objects.get(pk=3)
    rating = MovieRatingModel(id=5, movie=1726, rating=5, user=user)
    rating.save()

@shared_task
def calculateCosineSim(user_id):
    user = UserModel.objects.get(pk=user_id)
    movies_rating = MovieRatingModel.objects.filter(user=user)
    tv_rating = TvRatingModel.objects.filter(user=user)
    movie_ids = []
    for m in movies_rating:
        movie_ids.append(m.movie)

    tv_ids = []
    for t in tv_rating:
        tv_ids.append(t.tv)

    movie_qs: QuerySet = MovieRatingModel.objects.filter(movie__in=movie_ids)
    user_models = []


    for q in movie_qs:
        temp: QuerySet = movie_qs.filter(user__exact=q.user)
        if temp.count() > 4:
            user_models.append(q.user)
        movie_qs = movie_qs.exclude(user__exact=q.user)

    tv_qs: QuerySet = TvRatingModel.objects.filter(tv__in=tv_ids)

    for q in tv_qs:
        temp: QuerySet = tv_qs.filter(user__exact=q.user)
        if temp.count() > 4:
            if not q.user in user_models:
                user_models.append(q.user)
        tv_qs = tv_qs.exclude(user__exact=q.user)

    try:
        user_models.remove(user)
    except Exception as e:
        print(e)

    movie_qs: QuerySet = MovieRatingModel.objects.filter(movie__in=movie_ids)
    tv_qs: QuerySet = TvRatingModel.objects.filter(tv__in=tv_ids)

    for curr_user in user_models:
        query_cur_user = Q(user__exact=curr_user)
        print(curr_user.email)

        temp_movie = movie_qs.filter(query_cur_user)
        arr = []
        arr2 = []
        for row in temp_movie:
            arr2.append(row.rating)
            arr.append(movies_rating.get(movie__exact=row.movie).rating)



        temp_tv = tv_qs.filter(query_cur_user)
        for row in temp_tv:
            arr2.append(row.rating)
            arr.append(tv_rating.get(tv__exact=row.tv).rating)

        print(arr)
        print(arr2)
        vec_sim = cosine_similarity(np.array([arr, arr2]))
        similarity = vec_sim[0][1]
        print(similarity)

        try:
            query_user1 = Q(user1__exact=user)
            query_user2 = Q(user2__exact=curr_user)

            query_user2_2 = Q(user2__exact=user)
            query_user1_2 = Q(user1__exact=curr_user)

            sim_model: SimilarityModel = SimilarityModel.objects.get(query_user1 & query_user2)
            sim_model.similarity = similarity
            sim_model.save()
        except SimilarityModel.DoesNotExist:
            try:
                sim_model: SimilarityModel = SimilarityModel.objects.get(query_user1_2 & query_user2_2)
                sim_model.similarity = similarity
                sim_model.save()
            except SimilarityModel.DoesNotExist:
                sim_model = SimilarityModel(user1=user, user2=curr_user, similarity=similarity)
                sim_model.save()



@shared_task
def calculate_similarity(user_id):
    user = UserModel.objects.get(pk=user_id)
    movies_rating: MovieRatingModel = MovieRatingModel.objects.filter(user=user)
    tv_rating: TvRatingModel = TvRatingModel.objects.filter(user=user)
    movie_ids = []
    for m in movies_rating:
        movie_ids.append(m.movie)

    tv_ids = []
    for t in tv_rating:
        tv_ids.append(t.tv)

    print(movie_ids)
    print(tv_ids)

    qs: QuerySet = MovieRatingModel.objects.filter(movie__in=movie_ids)
    user_models = []

    for q in qs:
        temp: QuerySet = qs.filter(user__exact=q.user)
        if temp.count() > 5:
            user_models.append(q.user)
        qs = qs.exclude(user__exact=q.user)


    try:
        user_models.remove(user)
    except Exception as e:
        print(e)
    print(user_models)

    primary_su: QuerySet = StandardUnitsModel.objects.filter(user__exact=user)

    for curr_user in user_models:
        print("FOR USER:" + curr_user.email)
        sum = 0
        count = 0
        su_model: QuerySet = StandardUnitsModel.objects.filter(user__exact=curr_user)
        for su in su_model:
            try:
                query_title = Q(title_id__exact=su.title_id)
                query_type = Q(title_type__exact=su.title_type)
                su_instance = primary_su.get(query_title & query_type)
                sum = sum + (su.su * su_instance.su)
                count = count + 1
            except StandardUnitsModel.DoesNotExist:
                pass

        similarity = sum/count
        print("Sim: " + str(similarity))

        try:
            query_user1 = Q(user1__exact=user)
            query_user2 = Q(user2__exact=curr_user)

            query_user2_2 = Q(user2__exact=user)
            query_user1_2 = Q(user1__exact=curr_user)

            sim_model: SimilarityModel = SimilarityModel.objects.get(query_user1 & query_user2)
            sim_model.similarity = similarity
            sim_model.save()
        except SimilarityModel.DoesNotExist:
            try:
                sim_model: SimilarityModel = SimilarityModel.objects.get(query_user1_2 & query_user2_2)
                sim_model.similarity = similarity
                sim_model.save()
            except SimilarityModel.DoesNotExist:
                sim_model = SimilarityModel(user1=user, user2=curr_user, similarity=similarity)
                sim_model.save()

@shared_task
def calculate_user_su(user_id):
    print("For User: " + str(user_id))
    user = UserModel.objects.get(pk=user_id)
    movies: MovieRatingModel = MovieRatingModel.objects.filter(user__exact=user_id)
    tv: TvRatingModel = TvRatingModel.objects.filter(user__exact=user_id)

    sum = 0
    for m in movies:
        sum = sum + m.rating

    for t in tv:
        sum = sum + t.rating

    try:
        mean = sum / (len(movies) + len(tv))
    except Exception as e:
        mean = 0
    print(mean)

    sum = 0
    for m in movies:
        sum = sum + ((m.rating-mean) ** 2)

    for t in tv:
        sum = sum + ((t.rating-mean) ** 2)

    try:
        sqrt_avg = sqrt(sum/(len(movies) + len(tv)))
    except Exception as e:
        sqrt_avg = 0
    print("SQRT: " + str(sqrt_avg))

    query_user = Q(user__exact=user)
    query_movie = Q(title_type__exact=0)
    query_tv = Q(title_type__exact=1)
    for m in movies:
        if sqrt_avg == 0 or isnan(sqrt_avg):
            if m.rating == 1:
                su = -1
            elif m.rating == 5:
                su = 1
        else:
            su = (m.rating - mean)/sqrt_avg
        try:
            query_title = Q(title_id__exact=m.movie)
            instance: StandardUnitsModel = StandardUnitsModel.objects.get(query_title & query_user & query_movie)
            instance.su = su
            instance.save()
        except StandardUnitsModel.DoesNotExist:
            instance: StandardUnitsModel = StandardUnitsModel(user=user, title_id=m.movie, title_type=0, su=su)
            instance.save()

    for t in tv:
        if sqrt_avg == 0 or isnan(sqrt_avg):
            if m.rating == 1:
                su = -1
            elif m.rating == 5:
                su = 1
        else:
            su = (m.rating - mean)/sqrt_avg
        try:
            query_title = Q(title_id__exact=t.tv)
            instance: StandardUnitsModel = StandardUnitsModel.objects.get(query_title & query_user & query_tv)
            instance.su = su
            instance.save()
        except StandardUnitsModel.DoesNotExist:
            instance: StandardUnitsModel = StandardUnitsModel(user=user, title_id=t.tv, title_type=0, su=su)
            instance.save()
    print("finished")
    calculate_similarity.delay(user_id)

