from django.db import models
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from movies.models import Movie, Actor
from movies.serializers import MovieListSerializer, MovieDetailSerializer, ReviewCreateSerializer, \
    CreateRatingSerializer, ActorListSerializer, ActorDetailSerializer
from movies.service import get_client_ip, MovieFilter


class MovieListView(generics.ListAPIView):
    """Show list of movie"""

    serializer_class = MovieListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MovieFilter

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count('ratings', filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )
        return movies


# class MovieListView(APIView):
#     """Show list of movie"""
#
#     def get(self, request):
#         movies = Movie.objects.filter(draft=False).annotate(
#             rating_user=models.Count('ratings', filter=models.Q(ratings__ip=get_client_ip(request)))
#             # rating_user=models.Case(
#             #     models.When(ratings__ip=get_client_ip(request), then=True),
#             #     default=False,
#             #     output_field=models.BooleanField()
#             # )
#         ).annotate(
#             middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
#         )
#         serializer = MovieListSerializer(movies, many=True)  # many=True means that we have more than one record
#         return Response(serializer.data)


class MovieDetailView(generics.RetrieveAPIView):
    """Show movie"""

    queryset = Movie.objects.filter(draft=False)
    serializer_class = MovieDetailSerializer


# class ReviewCreateView(APIView):
#     """Add review"""
#
#     def post(self, request):
#         review = ReviewCreateSerializer(data=request.data)
#         if review.is_valid():
#             review.save()
#         return Response(status=201)


class ReviewCreateView(generics.CreateAPIView):
    """Add review"""

    serializer_class = ReviewCreateSerializer


class AddStarRatingView(generics.CreateAPIView):
    """Add star rating"""

    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


class ActorListView(generics.ListAPIView):
    """Get list of actors"""

    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer


class ActorDetailView(generics.RetrieveAPIView):
    """Get actor details """

    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer
