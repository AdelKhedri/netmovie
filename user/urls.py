from django.urls import path

# import Views
from .views import (ProfileView, ChangePasswordView, BuySubscriptionView, HistorySubscriptionView, TicketSupportView,
                    TicketDetailsView, RequestView, DashboardView)


app_name = 'dashboard'
urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('buy-subscription/', BuySubscriptionView.as_view(), name='buy-subscription'),
    path('history-subscription/', HistorySubscriptionView.as_view(), name='history-subscription'),
    path('ticket/', TicketSupportView.as_view(), name='ticket'),
    path('ticket/<int:ticket_id>/', TicketDetailsView.as_view(), name='ticket-details'),
    path('request/', RequestView.as_view(), name='request'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]
