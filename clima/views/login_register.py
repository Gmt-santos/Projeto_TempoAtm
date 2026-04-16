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
            cursor.execute("select name,password,icon,email,fav_city from users where email=%s",[_email])
            user_obj=cursor.fetchall()
            connection.close()
            # Gambiarra ----> força o python a verificar se tem algo nessa posicao
            if user_obj[0][3]:
                ...

        except IndexError:
            messages.error(request,"Login inválido")
            connection.close()
            return render(request,'html/login_clima.html')
            
        
       
        try:
            
            if ph.verify(user_obj[0][1],_password):
                context:dict={
                    "name":user_obj[0][0],
                    "auth":True,
                    "icon":user_obj[0][2],
                    "email":user_obj[0][3],
                    "fav_city":user_obj[0][4],
                } 
# O auth e o email sao responsabilidade do django e servem para salvar a sessao do usuario e o email dele
# assim,ninguem consegue entrar usando apenas a url. Não há nenhuma forma segura de fazer isso sem usar o django nesse caso
#
                request.session['email']=context["email"]
                request.session['auth']=True
                connection.close()
                return render(request,'html/intermediary_clima.html',context=context)
            
        except hash_exceptions.VerifyMismatchError:
            messages.error(request,"Login inválido")
            connection.close()
            return render(request,'html/login_clima.html')


    return render(request,'html/login_clima.html')

def login_out(request):
    request.session['auth']=False
    request.session['email']=None
    return render(request,'html/login_clima.html')




def register(request):
    return render(request,'html/register.html')



def register_operation(request):
    if request.method == "POST":
        load_dotenv()
        ph=PasswordHasher()
        HOST=os.getenv("HOST")
        USER=os.getenv("USER")
        PASSWORD=os.getenv("PASSWORD")
        DATABASE=os.getenv("DATABASE")
        # Porta padrao #
        port_=5432
        nome=request.POST.get("nome")
        email=request.POST.get("email")
        senha=request.POST.get("senha")
        confirmacao=request.POST.get("confirmacao_senha")
        icone=request.POST.get("select")
        if(senha == confirmacao and senha):
            try:
                connection=psycopg2.connect(host=HOST,user=USER,password=PASSWORD,database=DATABASE,port=port_)
                cursor=connection.cursor()
                cursor.execute("select email from users where email = %s",[email])
                user_obj=cursor.fetchall()
                if(user_obj):
                    # Já tem um email lá igual -----> TRATAR ERRO DEPOIS #
                    messages.error(request,"Login inválido")
                    connection.close()
                    return render(request,'html/login_clima.html')
                else:
                    hash_senha=ph.hash(senha)
                    cursor.execute("insert into users(name,password,icon,email)values(%s,%s,%s,%s)",[nome,hash_senha,icone,email])
                    connection.commit()
                    connection.close()
                    return render(request,'html/login_clima.html')
            except:
                ...

                ########### Continuar Trabalhando ##################



        