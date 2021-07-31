from rest_framework.response import Response
from rest_framework.views import APIView

from movies.models import Movie
from movies.serializers import MovieListSerializer, MovieDetailSerializer, ReviewCreateSerializer


class MovieListView(APIView):
    """Show list of movie"""

    def get(self, request):
        movies = Movie.objects.filter(draft=False)
        serializer = MovieListSerializer(movies, many=True)  # many=True means that we have more than one record
        return Response(serializer.data)


class MovieDetailView(APIView):
    """Show movie"""

    def get(self, request, pk):
        movie = Movie.objects.get(id=pk, draft=False)
        serializer = MovieDetailSerializer(movie)
        return Response(serializer.data)


class ReviewCreateView(APIView):
    """Add review"""

    def post(self, request):
        review = ReviewCreateSerializer(data=request.data)
        if review.is_valid():
            review.save()
        return Response(status=201)
