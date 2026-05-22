from django.shortcuts import render,redirect,get_object_or_404
from argon2 import PasswordHasher
from argon2 import exceptions as hash_exceptions
from django.contrib import messages
import datetime
from .. import utils
#Coleta as variaveis do .env#
import os

# postgre + python
import psycopg2



# Create your views here.
def login(request):
    context={
       
    }
    try:
        
        if(request.session["username"] and request.session["auth"]):
            return redirect("clima:dashboard_clima")
    except IndexError:
            return render(request,'html/login_clima.html')
    except KeyError:
            return render(request,'html/login_clima.html')
        #Procura na pasta templates DIRETAMENTE
        #Fica subentendido o templates/...
    

def login_enter(request):
    ph=PasswordHasher()
    HOST,USER,PASSWORD,DATABASE,port_=utils.load_var_env()
    if request.method == "POST":
        _email=request.POST.get("email")
        _password=request.POST.get("senha")

        
        try:
            
            connection=psycopg2.connect(host=HOST,user=USER,password=PASSWORD,database=DATABASE,port=port_)
            cursor=connection.cursor()
            cursor.execute("select users.name,users.password,users.icon,users.email,cities.name,username,users.id from users join " \
            "cities on users.fav_city=cities.id where users.email=%s",[_email])
            user_obj=cursor.fetchall()
       
            # força o python a verificar se tem algo nessa posicao
            if user_obj[0][3]:
                ...

        except IndexError:
            messages.error(request,"Esse email não está cadastrado ou a senha é inválida")
          
            return render(request,'html/login_clima.html')
        
        finally:
                if(connection is not None):
                    cursor.close()
                    connection.close()
        
            
        
       
        try:
            
            if ph.verify(user_obj[0][1],_password):
                request.session["name"]=user_obj[0][0]
                request.session["icon"]=user_obj[0][2]
                request.session["fav_city"]=user_obj[0][4]
                request.session["username"]=user_obj[0][5]
                request.session['id_user']=user_obj[0][6]
                hoje=datetime.date.today()
                mes_atual=hoje.month
                ano_atual=hoje.year
                dia_atual=hoje.day
                request.session["mes_atual"]=int(mes_atual)
                request.session["ano_atual"]=int(ano_atual)
                request.session["dia_atual"]=int(dia_atual)

                # O auth e o email sao responsabilidade do django e servem para salvar a sessao do usuario e o email dele
                # assim,ninguem consegue entrar usando apenas a url. 
                # Não há nenhuma forma segura de fazer isso sem usar o django nesse caso
                
                request.session['email']=user_obj[0][3]
                request.session['auth']=True
                
                return render(request,'html/intermediary_clima.html')
            
        except hash_exceptions.VerifyMismatchError:
            messages.error(request,"Esse email não está cadastrado ou a senha é inválida")
           
            return render(request,'html/login_clima.html')
        except Exception as error:
             messages.error(request,"Houve um erro inesperado na operação")
             return render(request,'html/login_clima.html')
        
        finally:
                if(connection is not None):
                    cursor.close()
                    connection.close()


    return render(request,'html/login_clima.html')

def login_out(request):
    request.session['auth']=False
    request.session['email']=None
    request.session.flush()
    return render(request,'html/login_clima.html')




def register(request):
    HOST,USER,PASSWORD,DATABASE,port_=utils.load_var_env()
    connection=psycopg2.connect(host=HOST,user=USER,password=PASSWORD,database=DATABASE,port=port_)
    cursor=connection.cursor()
    cursor.execute("select id,name,country,icon from cities")
    country_obj=cursor.fetchall()
    context={
        "cities":country_obj
    }
    
    return render(request,'html/register.html',context)



def register_operation(request):
    if request.method == "POST":
     
        ph=PasswordHasher()
        HOST,USER,PASSWORD,DATABASE,port_=utils.load_var_env()
        nome=request.POST.get("nome")
        email=request.POST.get("email")
        senha=request.POST.get("senha")
        confirmacao=request.POST.get("confirmacao_senha")
        icone=request.POST.get("select")
        username=request.POST.get("username")
        fav_city=request.POST.get("country")
        if(senha == confirmacao and senha):
            try:
                connection=psycopg2.connect(host=HOST,user=USER,password=PASSWORD,database=DATABASE,port=port_)
                cursor=connection.cursor()
                cursor.execute("select username,email from users where email = %s or username=%s",[email,username])
                user_obj=cursor.fetchall()
                if(user_obj):
                    # Já tem um email lá igual -----> TRATAR ERRO DEPOIS #
                    messages.error(request,"Esse email ou usuário já está cadastrado")
                    connection.close()
                    return render(request,'html/login_clima.html')
                else:
                    hash_senha=ph.hash(senha)
                    cursor.execute("insert into users(name,password,icon,fav_city,email,username)values(%s,%s,%s,%s,%s,%s)"
                                   ,[nome,hash_senha,icone,fav_city,email,username])
                    
                    connection.commit()
                    connection.close()
                    return render(request,'html/login_clima.html')
            except Exception as error:
                messages.error(request,"Houve um erro ao cadastrar,tente novamente mais tarde")
                return render(request,'html/login_clima.html')
            finally:
                if(connection is not None):
                    cursor.close()
                    connection.close()
                



def update_operation(request):
        try:
            if request.method == "POST":
                HOST,USER,PASSWORD,DATABASE,port_=utils.load_var_env()
                connection=psycopg2.connect(host=HOST,user=USER,password=PASSWORD,database=DATABASE,port=port_)
                cursor=connection.cursor()
                nome=request.POST.get("nome")
                icone=request.POST.get("select")
                fav_city=request.POST.get("country")
               
                username=request.POST.get("username")
                cursor.execute("update users set name=%s,icon=%s,fav_city=%s where username=%s",[nome,icone,fav_city,request.session["username"]])
                connection.commit()
                request.session["icon"]=icone
                request.session["name"]=nome
                connection.close()
                return redirect("clima:dashboard_clima")
            else:
               
                return redirect("clima:index")
        except Exception:
                return redirect("clima:dashboard")
        finally:
                if(connection is not None):
                    cursor.close()
                    connection.close()