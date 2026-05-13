from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
import os
from dotenv import load_dotenv
import psycopg2
from .. import utils
def create_event(request):
    load_dotenv()
    HOST=os.getenv("HOST")
    USER=os.getenv("USER")
    PASSWORD=os.getenv("PASSWORD")
    DATABASE=os.getenv("DATABASE")
     # Porta padrao #
    port_=5432
    connection=psycopg2.connect(host=HOST,user=USER,password=PASSWORD,database=DATABASE,port=port_)
    cursor=connection.cursor()
    cursor.execute("select id,name,country,icon,latitude,longitude from cities")
    country_obj=cursor.fetchall()
    context={
        "cities":country_obj
    }
    return render(request,'html/create_event.html',context=context)

def climate_query(request):
    id_city,lat,long=utils.retirar_id_lat_long(request.POST.get("country"))
    # API FAZER #
    context={
     "name":request.POST.get("name"),
     "descr":request.POST.get("descr"),
     "date_event":request.POST.get("date_event"),
     "hour_event":request.POST.get("hour_event"),
     "color":request.POST.get("color"),
     "icon":request.POST.get("select"),
    }
    return render(request,'html/climate_query.html',context=context)