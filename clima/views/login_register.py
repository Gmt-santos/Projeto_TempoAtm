from django.shortcuts import render,redirect,get_object_or_404
from argon2 import PasswordHasher
from argon2 import exceptions as hash_exceptions
from django.contrib import messages
#Coleta as variaveis do .env#
import os
from dotenv import load_dotenv
# postgre + python
import psycopg2

# Create your views here.




def login(request):
    context={
       
    }
    #Procura na pasta templates DIRETAMENTE
    #Fica subentendido o templates/...
    return render(request,'html/login_clima.html')

def login_enter(request):
   
    load_dotenv()
    ph=PasswordHasher()
    HOST=os.getenv("HOST")
    USER=os.getenv("USER")
    PASSWORD=os.getenv("PASSWORD")
    DATABASE=os.getenv("DATABASE")
    # Porta padrao #
    port_=5432
    if request.method == "POST":
        _email=request.POST.get("email")
        _password=request.POST.get("senha")

        
        try:

            connection=psycopg2.connect(host=HOST,user=USER,password=PASSWORD,database=DATABASE,port=port_)
            cursor=connection.cursor()
            cursor.execute("select name,password,icon,email from users where email=%s",[_email])
            user_obj=cursor.fetchall()

            # Gambiarra ----> força o python a verificar se tem algo nessa posicao
            if user_obj[0][3]:
                ...

        except IndexError:
            messages.error(request,"Login inválido")
            return render(request,'html/login_clima.html')
            
        
        
        try:
            if ph.verify(user_obj[0][1],_password):
                context:dict={
                    "name":user_obj[0][0],
                    "auth":True,
                    "icon":user_obj[0][2],
                    "email":user_obj[0][3],
                } 
                return render(request,'html/dashboard_clima.html',context=context)
            
        except hash_exceptions.VerifyMismatchError:
            messages.error(request,"Login inválido")
            return render(request,'html/login_clima.html')


            
            
        
        
                
        
    

    return render(request,'html/login_clima.html')
