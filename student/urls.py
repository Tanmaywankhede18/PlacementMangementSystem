from django.contrib import admin
from django.urls import path
from student import views

urlpatterns = [
    path('/Signout',views.signout),
    path('/dashboard', views.index),
    path('/Signup',views.signup),
    path('/Login', views.Signin, name="login"),
    path('/Register',views.register),
    # path('/dashboard/StudentProfile',views.ShowProfile),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', views.activate, name='activate'),  

]
