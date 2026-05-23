from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from .. import api
from .. import utils
from datetime import datetime,timedelta
import os
import psycopg2
import locale

def create_event(request):  
    connection=None
    try:
        if(request.session["email"] and request.session["name"]):
            HOST,USER,PASSWORD,DATABASE,port_=utils.load_var_env()
            connection=psycopg2.connect(host=HOST,user=USER,password=PASSWORD,database=DATABASE,port=port_)
            cursor=connection.cursor()
            cursor.execute("select id,name,country,icon,latitude,longitude from cities")
            country_obj=cursor.fetchall()
            context={
                "cities":country_obj
            }
            
            return render(request,'html/create_event.html',context=context)
    except psycopg2.OperationalError:
        messages.error(request,"Houve um erro ao consultar as informações,tente novamente mais tarde")
        return redirect("clima:dashboard_clima")
    except IndexError:
      
        return redirect("clima:dashboard_clima")
    finally:
        if connection is not None:
            cursor.close()
            connection.close()



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
                   
                    city_info = api.get_data(request=request,lat=lat,long=long)

                    '''
                    api.get_data retorna falso caso haja algum erro 
                    e retorna uma lista se tudo der certo
                    '''

                    if city_info:

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
                    messages.error(request,"Houve um erro com a comunicação do servidor OpenMeteo!")
                    return render(request,'html/climate_query.html',context=context)

            else:
               return redirect("clima:dashboard_clima")
        else:
            return redirect("clima:dashboard_clima")
    except IndexError:
        return redirect("clima:dashboard_clima")
    except KeyError:
        return redirect("clima:dashboard_clima")
    
    
    

def insert_event(request):
    connection=None
    if(request.method == "POST"):
        HOST,USER,PASSWORD,DATABASE,port=utils.load_var_env()
        
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
            cursor.execute("select id from types where icon =%s",[request.POST.get("select"),])
            icon_obj=cursor.fetchone()
            if not(icon_obj):
                return redirect("clima:dashboard_clima")
            icon_id=icon_obj[0]
            cursor.execute("insert into events(nome,descr,dia,hora,color,fk_type,fk_id_user,fk_city)values(" \
            "%s,%s,%s,%s,%s,%s,%s,%s);",[name,descr,date_event,hour_event,color,icon_id,request.session["id_user"],id_city])
            connection.commit()
            
            return redirect("clima:dashboard_clima")
        except psycopg2.OperationalError:
            return redirect("clima:dashboard_clima")
        except Exception :
            return redirect("clima:dashboard_clima")
        finally:
            if(connection is not None):
                cursor.close()
                connection.close()
    else:
        redirect("clima:dashboard_clima")

def query_event(request):
    connection=None
    if(request.session.get("email")):
        if(request.POST.get("name")):
            try:

                HOST,USER,PASSWORD,DATABASE,port=utils.load_var_env()
                connection=psycopg2.connect(host=HOST,user=USER,password=PASSWORD,database=DATABASE,port=port)
                cursor=connection.cursor()
                cursor.execute("select events.id,events.nome,events.dia,events.hora from events join users on events.fk_id_user=users.id" \
                " where users.id=%s and events.nome like %s",[request.session["id_user"],request.POST.get("name")+"%"])
                events=cursor.fetchall()
                context={
                    "events":events

                }
                
                return render(request,"html/query_event.html",context=context)
            
            except Exception as e:
                print(e)
                return redirect("clima:dashboard_clima")

            finally:
                if(connection is not None):
                    cursor.close()
                    connection.close()
        else:
            context={
                "events":None
            }
            return render(request,"html/query_event.html",context=context)
    else:
        return redirect("clima:index")
    
    
def form_event(request):
    if(request.method == "POST" and request.session.get("email")):
        try:

            HOST,USER,PASSWORD,DATABASE,port=utils.load_var_env()
            
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
            connection.close()
            context={
                "events":event,
                "cities":country_obj,
                "data_iso":data_iso,
            }
            return render(request,"html/form_event.html",context=context)
        
        except Exception:
    
             return redirect("clima:dashboard_clima")

        finally:
                if(connection is not None):
                    cursor.close()
                    connection.close()
    else:
       return  redirect("clima:dashboard_clima")
    


def update_event(request):
    if(request.method=="POST"):

        if(request.session.get("email") and request.session["id_user"] == int(request.POST.get("id_user")) ):
            
            try:
                HOST,USER,PASSWORD,DATABASE,port=utils.load_var_env()
                connection=psycopg2.connect(host=HOST,user=USER,password=PASSWORD,database=DATABASE,port=port)
                id_city,lat,long=utils.retirar_id_lat_long(request.POST.get("country"))
                cursor=connection.cursor()
                cursor.execute("select id from types where icon =%s",[request.POST.get("select"),])
                icon_obj=cursor.fetchone()
                if not(icon_obj):
                    return redirect("clima:dashboard_clima")
                icon_id=icon_obj[0]
                cursor.execute("update events set nome=%s,descr=%s,dia=%s,hora=%s,color=%s,fk_type=%s,fk_city=%s " \
                "where events.fk_id_user = %s and events.id= %s",
                [request.POST.get("name"),request.POST.get("descr"),request.POST.get("date_event"),request.POST.get("hour_event"),
                request.POST.get("color"),icon_id,id_city,request.session["id_user"],request.POST.get("id_event")])
                connection.commit() 
                connection.close()
                return redirect("clima:dashboard_clima")
            
            except Exception:
                redirect("clima:dashboard_clima")

            finally:
                if(connection is not None):
                    cursor.close()
                    connection.close()
            

        else:
            return redirect("clima:dashboard_clima")
        
    else:
        return redirect("clima:dashboard_clima")

def delete_event(request):
    if(request.method=="POST"):
        
        if(request.session.get("email") and request.session["id_user"] == int(request.POST.get("id_user"))):
            try:
                HOST,USER,PASSWORD,DATABASE,port=utils.load_var_env()
                connection=psycopg2.connect(host=HOST,user=USER,password=PASSWORD,database=DATABASE,port=port)
                cursor=connection.cursor()
                
                cursor.execute("delete from events where events.id=%s and events.fk_id_user=%s",[request.POST.get("id_event"),request.POST.get("id_user")])
                connection.commit()
                
                return redirect("clima:dashboard_clima")
            except Exception:
                 return redirect("clima:dashboard_clima")
            finally:
                if(connection is not None):
                    cursor.close()
                    connection.close()
        else:
            return redirect("clima:dashboard_clima")
    else:
        return redirect("clima:dashboard_clima")
    
def view_event(request,date):
    if(request.session.get("email") and request.session.get("id_user")):
         try:
            HOST,USER,PASSWORD,DATABASE,port=utils.load_var_env()
            connection=psycopg2.connect(host=HOST,user=USER,password=PASSWORD,database=DATABASE,port=port)
            cursor=connection.cursor()
            
            cursor.execute("select events.*,cities.name,cities.country,cities.latitude,cities.longitude,cities.icon " \
            "from events join cities on events.fk_city=cities.id where events.dia=%s and events.fk_id_user=%s",[date,request.session["id_user"]])
            events_obj=cursor.fetchall()
            context={
                "events":events_obj,
            }
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
            [9]->name(city)
            [10]->country(city)
            [11]->latitude
            [12]->longitude
            [13]->icon _country
            '''
            return render(request,"html/view_event.html",context=context)
         except Exception:
                
                 return redirect("clima:dashboard_clima")
         finally:
             if(connection is not None):
                cursor.close()
                connection.close()
    else:
        return redirect("clima:dashboard_clima")
    

def event_query_climate(request):
    connection=None
    try:

        if(request.method=="POST"):

            if(request.session["email"] and request.session["id_user"]):
                locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
                hoje=datetime.today()
                
                data_event=datetime.strptime(request.POST.get("date_event"),"%d de %B de %Y")
                
                diferenca:timedelta=data_event-hoje
                if(abs(int(diferenca.days))>=7):
                    HOST,USER,PASSWORD,DATABASE,port=utils.load_var_env()
                    connection=psycopg2.connect(host=HOST,user=USER,password=PASSWORD,database=DATABASE,port=port)
                    cursor=connection.cursor()
                    cursor.execute("select types.icon from types where types.id=%s ",[request.POST.get("fk_type"),])
                    icon_obj=cursor.fetchone()
                    if not(icon_obj):
                            return redirect("clima:dashboard_clima")
                    icon_img=icon_obj[0]
                    context={
                        'name':request.POST.get("name"),
                        'descr':request.POST.get("descr"),
                        'hour_event':request.POST.get('hour_event'),
                        'date_event':request.POST.get("date_event"),
                        'color':request.POST.get("color"),
                        # 'city_event':request.POST.get('city_event'), ?????
                        'city_name':request.POST.get("city_name"),
                        'city_country':request.POST.get("city_country"),
                        
                        'icon_country_img':request.POST.get("city_icon"),
                        'icon_event_img':icon_img,
                        'forecast_null':True,
                    }
                    return render(request,'html/event_query_climate.html',context=context)
                    
                    
                else:
                    data_event=datetime.strftime(data_event,"%Y-%m-%d")
                    intervalo_horas=utils.hora_evento(request)
                    city_info=api.get_data(request,request.POST.get("city_lat"),request.POST.get("city_long"),data_formatada=data_event)
                    condicao_climatica=utils.avaliacao_condicao_climatica(city_info,intervalo_horas)
                    HOST,USER,PASSWORD,DATABASE,port=utils.load_var_env()
                    connection=psycopg2.connect(host=HOST,user=USER,password=PASSWORD,database=DATABASE,port=port)
                    cursor=connection.cursor()
                    cursor.execute("select types.icon from types where types.id=%s ",[request.POST.get("fk_type"),])
                    icon_obj=cursor.fetchone()
                    if not(icon_obj):
                            return redirect("clima:dashboard_clima")
                    icon_img=icon_obj[0]
                    context={
                        'name':request.POST.get("name"),
                        'descr':request.POST.get("descr"),
                        'hour_event':request.POST.get('hour_event'),
                        'date_event':request.POST.get("date_event"),
                        'color':request.POST.get("color"),
                        'city_event':request.POST.get('city_event'),
                        'city_name':request.POST.get("city_name"),
                        'city_country':request.POST.get("city_country"),
                        'city_info':city_info,
                        'intervalo_horas':intervalo_horas,
                        'condicao_climatica':condicao_climatica,
                        'icon_country_img':request.POST.get("city_icon"),
                        'icon_event_img':icon_img,
                        'forecast_null':False,
                    }
                    return render(request,'html/event_query_climate.html',context=context)
                    



        else:
            return redirect("clima:dashboard_clima")
    except IndexError:
        return redirect("clima:dashboard_clima")
    except KeyError:
        return redirect("clima:dashboard_clima")
    finally:
        if connection is not None:
            cursor.close()
            connection.close()