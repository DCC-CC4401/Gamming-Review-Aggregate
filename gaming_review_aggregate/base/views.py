from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect


def home(request): #the homepage view
    if request.method == "GET":
       return render(request, "base/index.html")

def login(request): #the login view
    if request.method == "GET":
       return render(request, "base/login.html")

    elif request.method == 'POST': #Si estamos recibiendo el form de registro
        #Tomar los elementos del formulario que vienen en request.POST
        nombre = request.POST['nombre']
        password = request.POST['password']

        #Crear el nuevo usuario
        user = User.objects.create_user(username=nombre, password=password)

        #Redireccionar la página /home
        return HttpResponseRedirect('/home')

def popular_games(request): #the login view
    if request.method == "GET":
       return render(request, "base/popular-games.html")
