from django.urls import path

# import Views
from .views import ProfileView


app_name = 'dashboard'
urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile')
]