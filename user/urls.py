from django.urls import path

# import Views
from .views import ProfileView, ChangePasswordView, BuySubscriptionView, HistorySubscriptionView


app_name = 'dashboard'
urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('buy-subscription/', BuySubscriptionView.as_view(), name='buy-subscription'),
    path('history-subscription/', HistorySubscriptionView.as_view(), name='history-subscription'),
]
