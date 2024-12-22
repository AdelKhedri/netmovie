from django.urls import path
from .views import SerialDetailsView, MovieDetailsView, SerialGanerView, MovieGanerView, ActorsView, ActorDetailsView


urlpatterns = [
    path('serial/<str:slug>/', SerialDetailsView.as_view(), name='serial-details'),
    path('movie/<str:slug>/', MovieDetailsView.as_view(), name='movie-details'),
    path('serial/ganer/<str:slug>/', SerialGanerView.as_view(), name='serial-ganer'),
    path('movie/ganer/<str:slug>/', MovieGanerView.as_view(), name='movie-ganer'),
    path('actors', ActorsView.as_view(), name='actors'),
    path('actor/<int:id>/', ActorDetailsView.as_view(), name='actor-details'),
]
