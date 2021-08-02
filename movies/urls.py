from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views
from . import viewsets


urlpatterns = format_suffix_patterns([
    path('movie/', viewsets.MovieViewSet.as_view({'get': 'list'})),
    path('movie/<int:pk>/', viewsets.MovieViewSet.as_view({'get': 'retrieve'})),
    path('review/', viewsets.ReviewCreateViewSet.as_view({'post': 'create'})),
    path('rating/', viewsets.AddStarRatingViewSet.as_view({'post': 'create'})),
    path('actors/', viewsets.ActorViewSet.as_view({'get': 'list'})),
    path('actors/<int:pk>', viewsets.ActorViewSet.as_view({'get': 'retrieve'})),

])

# urlpatterns = [
#     path('movie/', views.MovieListView.as_view()),
#     path('movie/<int:pk>/', views.MovieDetailView.as_view()),
#     path('review/', views.ReviewCreateView.as_view()),
#     path('rating/', views.AddStarRatingView.as_view()),
#     path('actors/', views.ActorListView.as_view()),
#     path('actors/<int:pk>/', views.ActorDetailView.as_view()),
# ]
