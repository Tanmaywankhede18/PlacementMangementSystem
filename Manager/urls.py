from django.contrib import admin
from django.urls import path
from Manager import views

urlpatterns = [
    path('/Signout',views.signout),
    path('/dashboard', views.index),
    path('/Login', views.Login, name="login"),
    path('/Register',views.TPO),
    path('/dashboard/StudentProfile',views.ShowProfile),
    path('/Filter',views.Filter),
    path('/Profile/<str:prn>', views.ShowProfile),
    path('/PlacedFilter', views.PlacedFilter),
]
