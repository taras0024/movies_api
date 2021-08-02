from django.db import models
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.response import Response

from movies.models import Actor, Movie
from movies.serializers import ActorListSerializer, ActorDetailSerializer, MovieListSerializer, MovieDetailSerializer, \
    ReviewCreateSerializer, CreateRatingSerializer
from movies.service import MovieFilter, get_client_ip


# class ActorViewSet(viewsets.ViewSet):
#     def list(self, request):
#         queryset = Actor.objects.all()
#         serializer = ActorListSerializer(queryset, many=True)
#         return Response(serializer.data)
#
#     def retrieve(self, request, pk=None):
#         queryset = Actor.objects.all()
#         actor = get_object_or_404(queryset, pk=pk)
#         serializer = ActorDetailSerializer(actor)
#         return Response(serializer.data)


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    """Show list of movie"""

    filter_backends = (DjangoFilterBackend,)
    filterset_class = MovieFilter

    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count('ratings', filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )
        return movies

    def get_serializer_class(self):
        if self.action == 'list':
            return MovieListSerializer
        elif self.action == 'retrieve':
            return MovieDetailSerializer


class ReviewCreateViewSet(viewsets.ModelViewSet):
    """Add review"""

    serializer_class = ReviewCreateSerializer


class AddStarRatingViewSet(viewsets.ModelViewSet):
    """Add star rating"""

    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


class ActorViewSet(viewsets.ReadOnlyModelViewSet):
    """Get list of actors"""

    queryset = Actor.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ActorListSerializer
        elif self.action == 'retrieve':
            return ActorDetailSerializer
