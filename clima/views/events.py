from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages

def create_event(request):
    return render(request,'html/create_event.html')