from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name="appHome"),
    path('contacts/', views.contacts, name="contacts"),
    path('signup/', views.signup_method, name="signup"),
    path('login/', views.login_method, name="login"),
    path('logout/', views.logout_method, name="logout"),
    path('analyze/', views.analyze, name="analyze"),
    path('about/', views.about, name="about"),
    path('change_password/', views.change_password, name="change_password"),
    path('forgot_password/', views.forgot_password, name = "forgot_password"),
    
]
