from django.urls import path
from .views import SerialDetailsView


urlpatterns = [
    path('serial/<str:slug>/', SerialDetailsView.as_view(), name='serial-details'),
]