from django.shortcuts import render,redirect,get_object_or_404
from argon2 import PasswordHasher
from argon2 import exceptions as hash_exceptions
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
    #Provisorio#----> Configurar o sql
    load_dotenv()
    ph=PasswordHasher()
    HOST=os.getenv("HOST")
    USER=os.getenv("USER")
    PASSWORD=os.getenv("PASSWORD")
    DATABASE=os.getenv("DATABASE")
    # Porta padrao #
    port_=5432
    if request.method == "POST":
        email=request.POST.get("email")
        password=request.POST.get("senha")
        print(email)
        connection=psycopg2.connect(host=HOST,user=USER,password=PASSWORD,database=DATABASE,port=port_)
        cursor=connection.cursor()
        cursor.execute("select email,password from users where email=%s",[email])
        user_obj=cursor.fetchall()
        try:
            if ph.verify(user_obj[0][1],password):
                print("acertoooou")
        except hash_exceptions.VerifyMismatchError:
            print("merda")

            #### TRABALHANDO ###
            
        
        
                
        
    

    return render(request,'html/login_clima.html')
