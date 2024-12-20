from django.urls import path
from .views import SerialDetailsView, MovieDetailsView


urlpatterns = [
    path('serial/<str:slug>/', SerialDetailsView.as_view(), name='serial-details'),
    path('movie/<str:slug>/', MovieDetailsView.as_view(), name='movie-details'),
]
