from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
import datetime
import calendar
#Coleta as variaveis do .env#
import os
from dotenv import load_dotenv
# postgre + python
import psycopg2
from .. import utils

# Create your views here.
def intermediary_clima(request,_context:dict):
        #O intermediary_clima é usado apenas pelo programa,não tem motivo pra alguém entrar nele
        return redirect("clima:index")
    
def dashboard_clima(request):
     #Procura na pasta templates DIRETAMENTE
    #Fica subentendido o templates/...
     
     primeiro_dia,tamanho_calendario=utils.coletar_primeirodia_mes(request.session["ano_atual"],request.session["mes_atual"])
     
     try:
        if(request.session["auth"] ==  True):
            HOST,USER,PASSWORD,DATABASE,port_=utils.load_var_env()
            connection=psycopg2.connect(host=HOST,user=USER,password=PASSWORD,database=DATABASE,port=port_)
            cursor=connection.cursor()
            
            cursor.execute("select users.name,users.icon,users.email,users.fav_city,users.username " \
            "from users " \
            "where username=%s",[request.session["username"]])

            user_obj=cursor.fetchall()
            cursor.execute("select events.nome,events.dia,events.color,types.icon from events join users on users.id=events.fk_id_user" \
            " join types on events.fk_type=types.id where username =%s order by events.dia limit 5",[request.session["username"]])
            event_obj=cursor.fetchall()
            #Verifica se o email da url é o da sessao,evita que o cara invada outros emails com o auth=true
            if(user_obj[0][2] == request.session['email']):
                connection.close()
                events=[]
                
                try:
                    for event in event_obj:
                                    #nome       #dia    #cor    #icone
                     events.append([event[0],event[1],event[2],event[3]])
                except IndexError:
                     ...
               
                request.session["name"]=user_obj[0][0]
                request.session["icon"]=user_obj[0][1]
                request.session["fav_city"]=user_obj[0][3]
                request.session["username"]=user_obj[0][4]
                
               
                     
                context={
                     
                     "calendar_range":utils.lista_de_dias(primeiro_dia,tamanho_calendario),
                     "string_month":utils.string_mes(request.session["mes_atual"]),
                     "real_month":utils.mes_real(),
                     "real_year":utils.ano_real(),
                     "events":events
                }
                
                return render(request,'html/dashboard_clima.html',context=context)
            else:
                
                return redirect("clima:login")
        else:
            
            return redirect("clima:login")
    
     except KeyError:
         
         return redirect("clima:login")
     except IndexError:
         
         return redirect("clima:login")
     except psycopg2.OperationalError as error:
       
        messages.error(request,"Houve um erro ao cadastrar,tente novamente mais tarde")
        return render(request,'html/login_clima.html')
     finally:
            if(connection is not None):
                    cursor.close()
                    connection.close()
     
#FUNÇÕES PARA ATUALIZAR MES E DATA #

def update_month_plus(request):
     if request.session["mes_atual"] == 12:
          request.session["ano_atual"]+=1
          request.session["mes_atual"]=1
     else:
          request.session["mes_atual"]+=1
     return redirect("clima:dashboard_clima")

def update_month_minus(request):
      if request.session["mes_atual"] == 1:
          request.session["ano_atual"]-=1
          request.session["mes_atual"]=12
      else:
          request.session["mes_atual"]-=1
      return redirect("clima:dashboard_clima")


def perfil(request):
    try:
        if(request.session["auth"] == True):
                HOST,USER,PASSWORD,DATABASE,port_=utils.load_var_env()
                connection=psycopg2.connect(host=HOST,user=USER,password=PASSWORD,database=DATABASE,port=port_)
                cursor=connection.cursor()
                cursor.execute("select id,name,country,icon from cities")
                country_obj=cursor.fetchall()
                context={
                    "cities":country_obj
                }
    
                
                return render(request,"html/perfil.html",context)
    except psycopg2.OperationalError:
       
         return redirect("clima:dashboard_clima")
    except KeyError:
    
        return redirect("clima:login")
    finally:
                if(connection is not None):
                    cursor.close()
                    connection.close()