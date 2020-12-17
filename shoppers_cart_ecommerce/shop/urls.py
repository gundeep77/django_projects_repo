from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="ShopHome"),
    path("about/", views.about, name="AboutUs"),
    path("contacts/", views.contacts, name="ContactUs"),
    path("search/", views.search, name="Search"),
    path("tracker/", views.tracker, name="TrackingStatus"),
    path("productview/", views.productView, name="ProductView"),
    path("checkout/", views.checkout, name="Checkout"),

]
