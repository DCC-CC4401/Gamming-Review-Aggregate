from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q, Avg
from base.models import User, Game, Review, Friend_Request, Genre, GameMedia
import hashlib


games = Game.objects.all()
users = User.objects.all()
reviews = Review.objects.all()
friend_requests = Friend_Request.objects.all()
genre = Genre.objects.all()
fotos = GameMedia.objects.all()

def home(request): #the homepage view
    top_games = Game.objects.all().order_by('-promedio')
    if request.method == "GET":
        return render(request, "base/nav-bar/index.html", { "games": top_games, "users": users})


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


        # Dado un game, calcula su puntaje promedio
        def score(game):
            reviews = Review.objects.filter(game=game)
            try:
                prom = round(list(reviews.aggregate(Avg('score')).values())[0],1)
            except:
                prom = 0.0
            return prom


        # Clase que representa un objeto que contiene la información de un juego
        # que se va a mostrar en el listado de juegos
        class GameL:
            def __init__(self, game_id, name, plat, genres, score,foto):
                self.id = game_id
                self.name = name
                self.plataforma = plat
                self.genres = genres
                self.score = score
                self.foto = foto

        def getGameL(game):
            game_id = game.id
            game_name = game.nombre
            game_plat = game.plataforma
            game_genres = Genre.objects.filter(game=game)
            game_score = score(game)
            game_foto = GameMedia.objects.filter(game=game)[0].path

            return GameL(
                    game_id,
                    game_name,
                    game_plat,
                    game_genres,
                    game_score,
                    game_foto
                    )


        # armar una lista que contienen objetos con la información necesaria
        # Para mostrar listado de todos los juegos
        game_list = list(map(getGameL, games))

        return render(request, "base/nav-bar/popular-games.html", {"games": game_list })


def add_game(request): #the add game form view
    if request.method == "GET":
        return render(request, "base/nav-bar/agregar-juego.html")


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
    foto = request.FILES["foto"]

    # Acá hay que crear un código que, dado los datos anteriores, agregue a la base de datos el juego:
    game = Game.objects.create(nombre=nombre, anio=anio, descripcion=descripcion, desarrollador=desarrollador, plataforma=plat)
    games.update()

    # Se agrega géneros a la base de datos
    for g in gen:
        add_g = Genre.objects.create(name = g, game= game)

    # Se guarda la imagen con un nombre 
    total_images = GameMedia.objects.all().count()
    hash_archivo = str(total_images) + hashlib.sha256(
            foto.name.encode()).hexdigest()[0:30]
    file_path = './base/static/media/' + hash_archivo
    with open(file_path, 'wb') as image: 
        image.write(foto.file.read())

    # Se guarda la foto en la base de datos
    foto = GameMedia.objects.create(nombre = foto.name, path = hash_archivo, game = game)

    dic = {"nombre": nombre,
            "anio": anio,
            "descripcion": descripcion,
            "desarrollador": desarrollador,
            "plataforma": plat,
            "generos": gen,
            "foto": hash_archivo 
            }

    if request.method == "POST":
        return render(request, "base/resultados/juego-agregado.html", dic)


def perfilJuego(request):
    if request.method == "GET":
        nombre = request.GET["nombre"]
        resultado = Game.objects.filter(id=nombre)
        if (len(resultado)==0):
            return render(request, "base/resultados/perfil-juego.html", {"bol": 0})
        reviews = Review.objects.filter(game=nombre)
        generos = Genre.objects.filter(game=nombre)
        foto = GameMedia.objects.filter(game=nombre)
        try:
            prom = round(list(reviews.aggregate(Avg('score')).values())[0],1)
        except:
            prom = 0.0
        resultado.update(promedio=prom)
 
        return render(request, "base/resultados/perfil-juego.html", {
            "game": resultado[0], 
            "reviews": reviews,
            "generos": generos,
            "foto": foto[0],
            "bol": 1,
            "prom": prom}
            )

def validate_user_login(request): # Validador del nombre de usuario
    username = request.GET.get('username', None)    # Rescatamos 'username' del json entregado
    # Enviamos en otro json el resultado del validador
    invalid_user = False
    if (username == '' or len(username)<=1):
        invalid_user = True
    data = {
        'invalid_user': invalid_user
    }
    return JsonResponse(data)

def validate_passw_login(request): # Validador del nombre de usuario
    passw = request.GET.get('passw', None)    # Rescatamos 'passw' del json entregado
    # Enviamos en otro json el resultado del validador
    invalid_passw = False
    if (passw == '' or len(passw)<=1):
        invalid_passw = True
    data = {
        'invalid_passw': invalid_passw
    }
    return JsonResponse(data)

def validate_username(request): # Validador del nombre de usuario
    new_user = request.GET.get('username', None)    # Rescatamos 'username' del json entregado
    # Enviamos en otro json el resultado de buscar el nombre en la bbdd
    data = {
        'is_taken': User.objects.filter(username=new_user).exists()
    }
    return JsonResponse(data)

def validate_password(request): # Validador de la contraseña
    # Por ahora el validador solo varifica si es vacío o si el largo es mayor a 1
    # De querer agregar más validaciones, hay que añadir otros parámetros al if

    password = request.GET.get('password', None)    # Rescatamos 'password' del json entregado
    # Enviamos en otro json el resultado de buscar el nombre en la bbdd
    is_invalid = False
    if (password == '' or len(password) <= 1 or password == None):
        is_invalid = True
    data = {
        'is_invalid': is_invalid
    }
    return JsonResponse(data)

def validate_both_passwords(request): # Validador de la segunda contraseña
    password1 = request.GET.get('password1', None)    # Rescatamos 'password1' del json entregado
    password2 = request.GET.get('password2', None)    # Rescatamos 'password2' del json entregado
    # Verificamos si ambas entradas son iguales
    is_invalid = False
    if (password1 != password2 or password2 == ''):
        is_invalid = True
    data = {
        'is_invalid': is_invalid
    }
    return JsonResponse(data)

def validate_user(request): # Validador del usuario
    new_user = request.GET.get('username', None)    # Rescatamos 'username' del json entregado
    # Enviamos en otro json el resultado de buscar el nombre en la bbdd
    is_taken = False
    if (User.objects.filter(username=new_user).exists() or new_user == ''):
        is_taken = True
    data = {
        'is_taken': is_taken
    }
    return JsonResponse(data)

def cuentaCreada(request):
    new_user = request.POST["new-user"]
    new_password1 = request.POST["new-passw1"]
    new_password2 = request.POST["new-passw2"]

    #Acá hay que crear un código que, dado los datos anteriores, agregue a la base la nueva cuenta:
    #También se puede agregar acá el formato de los datos (usuario y contraseña) y su validación
    user = User.objects.create_user(username=new_user, nombre=new_user, password=new_password1)
    users.update()
    if request.method == "POST":
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
        return render(request, "base/resultados/cuenta-agregada.html", {"user": new_user})

def perfil(request): #the homepage view
    this_user = request.user
    this_friend_requests = Friend_Request.objects.filter(to_user=this_user)
    if request.method == "GET":
        return render(request, "base/perfil-usuario.html", {"reviews": reviews, "friend_requests": this_friend_requests, "user": request.user,"users": users})

    elif request.method == "POST":
        return render(request, "base/perfil-usuario.html", {"reviews": reviews, "friend_requests": this_friend_requests, "user": request.user, "users": users})

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

def add_review(request): #the add game form view
    if request.method == "GET":
        return render(request, "base/agregar-review.html", {"users" : users, "games": games})

def review_agregada(request):
    autor = request.user
    juego = request.POST["game"]
    puntaje = request.POST["score"]
    review = request.POST["game_review"]

    if request.user.is_authenticated:
        autor_user = User.objects.get(username=autor)
    else:
        autor_user, created = User.objects.get_or_create(username="Anonimo", nombre = "Anonimo", password = "nada")
        if created:
            autor_user.save()

    juego_obj = Game.objects.get(nombre=juego)
    review = Review.objects.create(author=autor_user, game=juego_obj, score=puntaje, body=review)
    reviews.update()

    game_reviews = reviews.filter(game=juego_obj)
    prom = round(list(game_reviews.aggregate(Avg('score')).values())[0],1)
    thegame = games.filter(nombre=juego)
    thegame.update(promedio=prom)
    if request.method == "POST":
        review.save()
        return render(request, "base/resultados/review-agregada.html", {"user": autor})

@login_required
def send_friend_request(request, userID):
    from_user = request.user
    to_user = User.objects.get(id=userID)
    friend_request, created = Friend_Request.objects.get_or_create(from_user=from_user, to_user=to_user)
    if created:
        return HttpResponse('friend request sent')
    else:
        return HttpResponse('friend request was already sent')

@login_required
def accept_friend_request(request, requestID):
    friend_request = Friend_Request.objects.get(id=requestID)
    if friend_request.to_user == request.user:
        friend_request.to_user.friends.add(friend_request.from_user)
        friend_request.from_user.friends.add(friend_request.to_user)
        friend_request.delete()
        return HttpResponse('friend request accepted')
    else:
        return HttpResponse('friend request not accepted')
