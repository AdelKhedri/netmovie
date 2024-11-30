# For statics
from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
from django.urls import path
from user.views import LoginView, home


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('home', home, name='home'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
