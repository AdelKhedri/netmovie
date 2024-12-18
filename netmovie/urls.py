# For statics
from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
from django.urls import include, path
from user.views import LoginView, SignupView, logoutView
from movieserial.views import HomeView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('', HomeView.as_view(), name='home'),
    path('logout', logoutView, name='logout'),
    path('dashboard/', include('user.urls')),
    path('', include('movieserial.urls')),
]
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
