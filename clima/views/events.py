from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from .. import api
from .. import utils
from datetime import datetime,timedelta
import os
from dotenv import load_dotenv
import psycopg2

def create_event(request):  
    try:
        if(request.session["email"] and request.session["name"]):
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
    except psycopg2.OperationalError:
        connection.close()
        redirect("clima:dashboard_clima")
    except IndexError:
        connection.close()
        redirect("clima:dashboard_clima")
    except KeyError:
        connection.close()
        redirect("clima:dashboard_clima")



def climate_query(request):
    try:

        if(request.method=="POST"):

            if(request.session["email"] and request.session["name"]):
                hoje=datetime.today()
                data_event=datetime.strptime(request.POST.get("date_event"),"%Y-%m-%d")
                diferenca:timedelta=data_event-hoje


                id_city,lat,long=utils.retirar_id_lat_long(request.POST.get("country"))


                # Distância máxima para uma melhor eficácia do OpenMeteo
                if(diferenca.days>=7):
                    context={
                        "name":request.POST.get("name"),
                        "descr":request.POST.get("descr"),
                        "date_event":request.POST.get("date_event"),
                        "hour_event":request.POST.get("hour_event"),
                        "color":request.POST.get("color"),
                        "icon":request.POST.get("select"),
                        "id_city":id_city,
                        "forecast_null":True
                    }
                    return render(request,'html/climate_query.html',context=context)
                else:
                   
                    city_info:list = api.get_data(request=request,lat=lat,long=long)
                    intervalo_horas=utils.hora_evento(request=request)
                    condicao_climatica=utils.avaliacao_condicao_climatica(city_info,intervalo_horas)
                    '''
                    cityinfo
                    [0]->Temperatura
                    [1]->Umidade relativa
                    [2]->Temperatura aparente
                    [3]->Probabilidade de chuva
                    [4]->Chuva
                    [5]->Cobertura por nuvens
                    [6]->Velocidade do vento
                    
                    '''
                    '''
                    condiçao climatica
                    [0]-> cor
                    [1]-> icone
                    [2]-> Titulo
                    [3]-> Descriçao
                    '''
                    context={
                    "name":request.POST.get("name"),
                    "descr":request.POST.get("descr"),
                    "date_event":request.POST.get("date_event"),
                    "hour_event":request.POST.get("hour_event"),
                    "color":request.POST.get("color"),
                    "icon":request.POST.get("select"),
                    "id_city":id_city,
                    "forecast_null":False,
                    "city_info":city_info,
                    "intervalo_horas":intervalo_horas,
                    "condicao_climatica":condicao_climatica
                    }
                    return render(request,'html/climate_query.html',context=context)
        else:
            return redirect("clima:dashboard_clima")
    except IndexError:
        return redirect("clima:dashboard_clima")
    except KeyError:
        return redirect("clima:dashboard_clima")
    

def insert_event(request):
    if(request.method == "POST"):
        load_dotenv()
        HOST=os.getenv("HOST")
        USER=os.getenv("USER")
        PASSWORD=os.getenv("PASSWORD")
        DATABASE=os.getenv("DATABASE")
        port=5432
        
        name=request.POST.get("name")
        descr=request.POST.get("descr")
        date_event=request.POST.get("date_event")
        hour_event=request.POST.get("hour_event")
        color=request.POST.get("color")
        icon=request.POST.get("select")
        id_city=request.POST.get("id_city")
        try:
            connection=psycopg2.connect(host=HOST,user=USER,password=PASSWORD,database=DATABASE,port=port)
            cursor=connection.cursor()
            cursor.execute("select id from types where icon =%s",[icon,])
            icon_id=cursor.fetchone()[0]
            cursor.execute("insert into events(nome,descr,dia,hora,color,fk_type,fk_id_user,fk_city)values(" \
            "%s,%s,%s,%s,%s,%s,%s,%s);",[name,descr,date_event,hour_event,color,icon_id,request.session["id_user"],id_city])
            connection.commit()
            connection.close()
            return redirect("clima:dashboard_clima")
        except psycopg2.OperationalError:
            return redirect("clima:dashboard_clima")
        except KeyError:
            return redirect("clima:dashboard_clima")
    else:
        redirect("clima:dashboard_clima")

def query_event(request):
    if(request.session.get("email")):
        if(request.POST.get("name")):
            load_dotenv()
            HOST=os.getenv("HOST")
            USER=os.getenv("USER")
            PASSWORD=os.getenv("PASSWORD")
            DATABASE=os.getenv("DATABASE")
            port=5432
            connection=psycopg2.connect(host=HOST,user=USER,password=PASSWORD,database=DATABASE,port=port)
            cursor=connection.cursor()
            cursor.execute("select events.id,events.nome,events.dia,events.hora from events join users on events.fk_id_user=users.id" \
            " where users.id=%s and events.nome like %s",[request.session["id_user"],request.POST.get("name")])
            events=cursor.fetchall()
            context={
                "events":events

            }
            return render(request,"html/query_event.html",context=context)
        else:
            context={
                "events":None
            }
            return render(request,"html/query_event.html",context=context)
    else:
        return redirect("clima:index")
    
    
def form_event(request):
    if(request.method == "POST" and request.session.get("email")):
        load_dotenv()
        HOST=os.getenv("HOST")
        USER=os.getenv("USER")
        PASSWORD=os.getenv("PASSWORD")
        DATABASE=os.getenv("DATABASE")
        port=5432
        connection=psycopg2.connect(host=HOST,user=USER,password=PASSWORD,database=DATABASE,port=port)
        cursor=connection.cursor()
        cursor.execute("select events.* from events where events.id=%s",[request.POST.get("id_event"),])
        event=cursor.fetchone()
        '''
        event
        [0]->id
        [1]->nome
        [2]->descr
        [3]->dia
        [4]->hora
        [5]->color
        [6]->fk_type
        [7]->fk_id_user
        [8]->fk_city

        '''
        data_iso=event[3]
        data_iso=data_iso.isoformat()
        cursor.execute("select id,name,country,icon,latitude,longitude from cities")
        country_obj=cursor.fetchall()
        
        context={
            "events":event,
            "cities":country_obj,
            "data_iso":data_iso,
        }
        return render(request,"html/form_event.html",context=context)
    else:
        redirect("clima:dashboard_clima")
    
def update_event(request):
    ...
def delete_event(request):...