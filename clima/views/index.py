from django.shortcuts import render,redirect,get_object_or_404


# Create your views here.
def index(request):
    context={
       
    }
    #Procura na pasta templates DIRETAMENTE
    #Fica subentendido o templates/...
    return render(request,'html/index_clima.html')