# For statics
from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
from django.urls import include, path
from user.views import LoginView, SignupView, logoutView, home


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('home', home, name='home'),
    path('logout', logoutView, name='logout'),
    path('dashboard/', include('user.urls')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
