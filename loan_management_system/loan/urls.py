from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = "home"),
    path('customer_signin/', views.customer_signin, name = "customer_signin"),
    path('customer_signout/', views.customer_signout, name = "customer_signout"),
    path('customer_signup/', views.customer_signup, name = "customer_signup"),
    path('agent_signin/', views.agent_signin, name = "agent_signin"),
    path('agent_signout/', views.agent_signout, name = "agent_signout"),
    path('admin_signin/', views.admin_signin, name = "admin_signin"),
    path('admin_signout/', views.admin_signout, name = "admin_signout"),
    path('customer_signin/loan_request/', views.loan_request, name = "new_loan"),
    path('customer_signin/change_password/', views.change_password, name="change_password"),
]
