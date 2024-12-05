from django.urls import path

# import Views
from .views import ProfileView, ChangePasswordView


app_name = 'dashboard'
urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]
