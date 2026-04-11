from django.contrib import admin
from django.urls import path
from clima import views
app_name="clima"
urlpatterns = [
    path('', views.index,name="index"),
    path('login/',views.login,name="login"),
    path('login/enter/',views.login_enter,name="login_enter")
]