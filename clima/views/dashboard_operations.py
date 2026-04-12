from django.shortcuts import render,redirect,get_object_or_404


# Create your views here.
def dashboard_clima(request,_context:dict={}):
     #Procura na pasta templates DIRETAMENTE
    #Fica subentendido o templates/...
    if not _context:
        # Proibe o usuário de entrar no dashboard sem um dict de context
        return redirect("clima:index")
    if(_context["auth"] ==  True):
        return render(request,'html/dashboard_clima.html',context=_context)
    else:
        return redirect("clima:index")
     