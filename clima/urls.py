from django.contrib import admin
from django.urls import path
from clima import views
app_name="clima"
urlpatterns = [
    path('', views.index,name="index"),
    path('login/',views.login,name="login"),
    path('login/enter/',views.login_enter,name="login_enter"),
    path('login/out/',views.login_out,name="login_out"),
    path('dashboard_clima/<str:email>/',views.dashboard_clima,name="dashboard_clima"),
    path('intermediary_clima/<str:email>/',views.intermediary_clima,name="intermediary_clima"),
    path('register/',views.register,name="register")
]