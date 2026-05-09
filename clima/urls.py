from django.contrib import admin
from django.urls import path
from clima import views
app_name="clima"
urlpatterns = [
    path('', views.index,name="index"),
    path('login/',views.login,name="login"),
    path('login/enter/',views.login_enter,name="login_enter"),
    path('login/out/',views.login_out,name="login_out"),
    path('dashboard_clima/',views.dashboard_clima,name="dashboard_clima"),
    path('intermediary_clima/',views.intermediary_clima,name="intermediary_clima"),
    path('register/',views.register,name="register"),
    path('register/operation',views.register_operation,name="register_operation"),
    path('update/operation',views.update_operation,name="update_operation"),
    path('dashboard_clima/perfil/',views.perfil,name="perfil")
]
