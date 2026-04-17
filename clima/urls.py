from django.contrib import admin
from django.urls import path
from clima import views
app_name="clima"
urlpatterns = [
    path('', views.index,name="index"),
    path('login/',views.login,name="login"),
    path('login/enter/',views.login_enter,name="login_enter"),
    path('login/out/',views.login_out,name="login_out"),
    path('dashboard_clima/<str:username>/',views.dashboard_clima,name="dashboard_clima"),
    path('intermediary_clima/<str:username>/',views.intermediary_clima,name="intermediary_clima"),
    path('register/',views.register,name="register"),
    path('register/operation',views.register_operation,name="register_operation"),
    path('dashboard_clima/perfil/<str:username><str:icon>/',views.perfil,name="perfil")
]
