from django.urls import path
from epicQuiz import views


urlpatterns = [
    path('', views.home, name = 'home'),
    path('computer_quiz/', views.computer_quiz, name = "computer_quiz"),
    path('science_quiz/', views.science_quiz, name = "science_quiz"),
    path('gk_quiz/', views.gk_quiz, name = "gk_quiz"),
    path('user/', views.user_page, name = "user_page"),
    path('computer_quiz/result/', views.computer_result, name = "r_computer"),
    path('science_quiz/result/', views.science_result, name = "r_science"),
    path('gk_quiz/result/', views.gk_result, name = "r_gk"),
    path('login/', views.login_method, name = "login"),
    path('signup/', views.signup_method, name = "signup"),
    path('user/logout/', views.logout_method, name = "logout"),
    path('user/change_password/', views.change_password, name = "change_password"),
    path('forgot_password/', views.forgot_password, name = "forgot_password"),

]
