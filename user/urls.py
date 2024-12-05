from django.urls import path

# import Views
from .views import ProfileView, ChangePasswordView, BuySubscriptionView


app_name = 'dashboard'
urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('buy-subscription/', BuySubscriptionView.as_view(), name='buy-subscription'),
]
