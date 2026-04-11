from django.shortcuts import render,redirect,get_object_or_404


# Create your views here.
def login(request):
    context={
       
    }
    #Procura na pasta templates DIRETAMENTE
    #Fica subentendido o templates/...
    return render(request,'html/login_clima.html')

def login_enter(request):
    #Provisorio#----> Configurar o sql
    return render(request,'html/login_clima.html')
