from django.urls import path
from .views import (SerialDetailsView, MovieDetailsView, SerialGanerView, MovieGanerView, ActorsView, ActorDetailsView, ContactUsView,
    AllMoviesView, AllSerialsView
    )


app_name = 'media'
urlpatterns = [
    path('movie/', AllMoviesView.as_view(), name='movies'),
    path('serial/', AllSerialsView.as_view(), name='serials'),
    path('serial/<str:slug>/', SerialDetailsView.as_view(), name='serial-details'),
    path('movie/<str:slug>/', MovieDetailsView.as_view(), name='movie-details'),
    path('serial/ganer/<str:slug>/', SerialGanerView.as_view(), name='serial-ganer'),
    path('movie/ganer/<str:slug>/', MovieGanerView.as_view(), name='movie-ganer'),
    path('actors', ActorsView.as_view(), name='actors'),
    path('actor/<int:id>/', ActorDetailsView.as_view(), name='actor-details'),
    path('contact-us/', ContactUsView.as_view(), name='contact-us'),
]
