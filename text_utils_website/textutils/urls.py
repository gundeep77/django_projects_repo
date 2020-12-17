from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from tuapp import views

urlpatterns = [
    path('', views.home, name="home"),
    path('tuapp/', include('tuapp.urls')),
    path('admin/', admin.site.urls),
    # path(r'session_security/', include('session_security.urls')),

]