from django.contrib import admin
from django.urls import path
from clima import views
app_name="clima"
urlpatterns = [
    path('', views.index,name="index"),

    path('login/',views.login,name="login"),
    path('login/enter/',views.login_enter,name="login_enter"),
    path('login/out/',views.login_out,name="login_out"),
    path('intermediary_clima/',views.intermediary_clima,name="intermediary_clima"),

    path('register/',views.register,name="register"),
    path('register/operation',views.register_operation,name="register_operation"),

    path('dashboard_clima/',views.dashboard_clima,name="dashboard_clima"),
    path('dashboard_clima/month_plus/',views.update_month_plus,name="update_month_plus"),
    path('dashboard_clima/month_minus/',views.update_month_minus,name="update_month_minus"),
    path('dashboard_clima/create_event/',views.create_event,name="create_event"),
    path('dashboard_clima/create_event/climate_query/',views.climate_query,name="climate_query"),
    path('dashboard_clima/create_event/insert_event/',views.insert_event,name="insert_event"),
    path('dashboard_clima/edit_event/query_event/',views.query_event,name="query_event"),
    path('dashboard_clima/edit_event/form_event/',views.form_event,name="form_event"),
    path('dashboard_clima/edit_event/update_event/',views.update_event,name="update_event"),
    path('dashboard_clima/edit_event/delete_event/',views.delete_event,name="delete_event"),
    path('dashboard_clima/view_event/<str:date>/',views.view_event,name="view_event"),


    path('update/operation',views.update_operation,name="update_operation"),
    path('dashboard_clima/perfil/',views.perfil,name="perfil")
    
]
