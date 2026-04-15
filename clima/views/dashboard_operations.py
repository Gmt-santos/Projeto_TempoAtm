from django.shortcuts import render,redirect,get_object_or_404
#Coleta as variaveis do .env#
import os
from dotenv import load_dotenv
# postgre + python
import psycopg2

# Create your views here.
def intermediary_clima(request,_context:dict):
  
        return redirect("clima:index")
    
def dashboard_clima(request,email:str):
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
            cursor.execute("select name,icon,email,fav_city from users where email=%s",[email])
            user_obj=cursor.fetchall()
            #Verifica se o email da url é o da sessao,evita que o cara invada outros emails com o auth=true
            if(email == request.session['email']):
                context:dict={
                            "name":user_obj[0][0],
                            "auth":True,
                            "icon":user_obj[0][1],
                            "email":user_obj[0][2],
                            "fav_city":user_obj[0][3],
                        } 
                return render(request,'html/dashboard_clima.html',context=context)
            else:
                return redirect("clima:index")
        else:
            return redirect("clima:index")
    #Caso a pessoa tente entrar sem nem ter auth
    except KeyError:
         return redirect("clima:login")