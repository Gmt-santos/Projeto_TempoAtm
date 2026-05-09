from django.shortcuts import render,redirect,get_object_or_404
#Coleta as variaveis do .env#
import os
from dotenv import load_dotenv
# postgre + python
import psycopg2
from django.contrib import messages

# Create your views here.
def intermediary_clima(request,_context:dict):
        #O intermediary_clima é usado apenas pelo programa,não tem motivo pra alguém entrar nele
        return redirect("clima:index")
    
def dashboard_clima(request):
     #Procura na pasta templates DIRETAMENTE
    #Fica subentendido o templates/...
     try:
        if(request.session["auth"] ==  True):
            load_dotenv()
            HOST=os.getenv("HOST")
            USER=os.getenv("USER")
            PASSWORD=os.getenv("PASSWORD")
            DATABASE=os.getenv("DATABASE")
            port_=5432
            connection=psycopg2.connect(host=HOST,user=USER,password=PASSWORD,database=DATABASE,port=port_)
            cursor=connection.cursor()
            
            cursor.execute("select name,icon,email,fav_city,username from users where username=%s",[request.session["username"]])
            user_obj=cursor.fetchall()
            #Verifica se o email da url é o da sessao,evita que o cara invada outros emails com o auth=true
            if(user_obj[0][2] == request.session['email']):
                request.session["name"]=user_obj[0][0]
                request.session["icon"]=user_obj[0][1]
                request.session["fav_city"]=user_obj[0][3]
                request.session["username"]=user_obj[0][4]
                connection.close()
                return render(request,'html/dashboard_clima.html')
            else:
                connection.close()
                return redirect("clima:login")
        else:
            connection.close()
            return redirect("clima:login")
    
     except KeyError:
         connection.close()
         return redirect("clima:login")
     except IndexError:
         connection.close()
         return redirect("clima:login")
     except psycopg2.OperationalError as error:
        connection.close()
        messages.error(request,"Houve um erro ao cadastrar,tente novamente mais tarde")
        return render(request,'html/login_clima.html')
     
def perfil(request):
    try:
        if(request.session["auth"] == True):
                load_dotenv()
                HOST=os.getenv("HOST")
                USER=os.getenv("USER")
                PASSWORD=os.getenv("PASSWORD")
                DATABASE=os.getenv("DATABASE")
                 # Porta padrao #
                port_=5432
                connection=psycopg2.connect(host=HOST,user=USER,password=PASSWORD,database=DATABASE,port=port_)
                cursor=connection.cursor()
                cursor.execute("select id,name,country,icon from cities")
                country_obj=cursor.fetchall()
                context={
                    "cities":country_obj
                }
    
                connection.close()
                return render(request,"html/perfil.html",context)
    except psycopg2.OperationalError:
         connection.close()
         return redirect("clima:dashboard_clima")
    except KeyError:
        connection.close()
        return redirect("clima:login")