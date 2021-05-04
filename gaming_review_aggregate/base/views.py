from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.db.models import Q

from base.models import User, Game


plataforms = ["Android", "Arcade", "Atari",
        "Game Boy", "Game Boy Advance", "Game Boy Color",
        "Nintendo 3DS", "Nintendo 64", "Nintendo DS", "Nintendo DSi",
        "Nintendo Entertainment System (NES)", "Nintendo GameCube",
        "Nintendo Switch", "PC", "PlayStation", "PlayStation 2", "PlayStation 3",
        "PlayStation 4", "PlayStation 5", "PlayStation Portable (PSP)", "Sega",
        "Super Nintendo Entertainment System (SNES)", "Wii", "Wii U",
        "Xbox", "Xbox 360", "Xbox One", "Xbox Series", "Other"
        ]

genres = ["Action", "Adventure", "Fighting", "Platform",
        "Puzzle", "Racing", "Role-playing", "Shooter", "Simulation",
        "Sports", "Strategy", "Other"]

games = Game.objects.all()
usuarios = User.objects.all()


def home(request): #the homepage view
    if request.method == "GET":
        return render(request, "base/nav-bar/index.html", { "games": games, "usuarios": usuarios})

def user_login(request): #the login view
    if request.method == "GET":
       return render(request, "base/nav-bar/login.html")

    elif request.method == 'POST': #Si estamos recibiendo el form de registro
        #Tomar los elementos del formulario que vienen en request.POST
        username = request.POST['user']
        contraseña = request.POST['passw']

        #Autenticar al usuario
        user = authenticate(username=username, nombre=username, password=contraseña)

        if user is not None:
            #Redireccionar la página /home
            #login(request, user)
            if user.is_active:
                login(request,user)
                user.last_login = timezone.now()
                user.save(update_fields=['last_login'])
                return HttpResponseRedirect('/home')
            else:
                return HttpResponseRedirect('/add_game')
        else:
            print("invalid login details " + username + " " + contraseña)
            return HttpResponseRedirect('/login')

def user_logout(request):
    logout(request)
    # Redirect back to index page.
    return render(request, "base/resultados/sesion-cerrada.html")

def popular_games(request): # the popular games view
    if request.method == "GET":
        return render(request, "base/nav-bar/popular-games.html", {"genres" : genres, "games": games})

def add_game(request): #the add game form view
    if request.method == "GET":
        return render(request, "base/nav-bar/agregar-juego.html", {"plataforms": plataforms, "genres": genres})

def buscar(request):
    buscado = request.GET["search"]
    resultados = Game.objects.filter(Q(nombre__icontains=buscado) | Q(desarrollador__icontains=buscado) | Q(genero__icontains=buscado))

    if request.method == "GET":
        #Cuando se haga la consulta respecto al nombre buscado, hay que agregar los resultados en el diccionario, tipo:
        #return render(request, "base/buscar-nombre.html", {"buscado": nombre, "resultados": resultados})
        return render(request, "base/resultados/nombre-buscado.html", {"buscado": buscado, "resultados": resultados})

def juegoAgregado(request):
    nombre = request.POST["nombre"]
    anio = request.POST["anio"]
    descripcion = request.POST["descripcion"]
    desarrollador = request.POST["dev"]
    plat = request.POST["plat"]
    gen = request.POST.getlist("gen")

    dic = {"nombre": nombre, 
            "anio": anio,
            "descripcion": descripcion,
            "desarrollador": desarrollador,
            "plataforma": plat,
            "generos": gen
            }

    #Acá hay que crear un código que, dado los datos anteriores, agregue a la base de datos el juego:
    game = Game.objects.create(nombre=nombre, anio=anio, descripcion=descripcion, desarrollador=desarrollador, plataforma=plat, genero=gen)
    games.update()
    if request.method == "POST":
        return render(request, "base/resultados/juego-agregado.html", dic)

def perfilJuego(request):
    nombre = request.GET["nombre"]
    resultado = Game.objects.filter(id=nombre)
    print(resultado)
    if request.method == "GET":
        return render(request, "base/resultados/perfil-juego.html", {"game": resultado})

def cuentaCreada(request):
    new_user = request.POST["new-user"]
    new_password1 = request.POST["new-passw1"]
    new_password2 = request.POST["new-passw2"]

    #Acá hay que crear un código que, dado los datos anteriores, agregue a la base la nueva cuenta:
    #También se puede agregar acá el formato de los datos (usuario y contraseña) y su validación
    user = User.objects.create_user(username=new_user, nombre=new_user, password=new_password1)

    if request.method == "POST":
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
        return render(request, "base/resultados/cuenta-agregada.html", {"user": new_user})

def perfil(request): #the homepage view
    if request.method == "GET":
        return render(request, "base/perfil-usuario.html")

    elif request.method == "POST":
        return render(request, "base/perfil-usuario.html")

def editar_perfil(request): #the homepage view
    if request.method == "GET":
        return render(request, "base/editar-perfil.html")

def perfil_actualizado(request):
    edit_edad = request.POST["edad"]
    edit_correo = request.POST["correo"]
    edit_descripcion_usuario = request.POST["descripcion_usuario"]

    usuario = request.user
    usuario.edad = edit_edad
    usuario.email = edit_correo
    usuario.descripcion = edit_descripcion_usuario
    usuario.save(update_fields=["edad","email","descripcion"])
    return redirect('perfil/')

