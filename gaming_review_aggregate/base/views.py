from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q, Avg
from base.models import User, Game, Review, Friend_Request, Genre, GameMedia, UserMedia
import hashlib
from os import remove


games = Game.objects.all() # Todos los juegos de la base de datos
users = User.objects.all() # Todos los usuarios de la base de datos
reviews = Review.objects.all() # Todas las reseñas de la base de datos
friend_requests = Friend_Request.objects.all() # Todas las solicitudes de amistad
genre = Genre.objects.all() # Todos los géneros de la base de datos
fotos = GameMedia.objects.all() # Todas las fotos (de juegos) de la base de datos


def home(request): # Vista de la página de home
    users = User.objects.all() # Todos los usuarios de la base de datos
    top_games = games.order_by('-promedio')[:5] # Filtra los mejores juegos
    game_list = list(map(createGameL, top_games)) # Mapea la lista de mejores juegos

    user = request.user
    users_r = []

    if not (user.is_anonymous):
        users_raw = User.objects.exclude(nombre=user)
        friend_request = Friend_Request.objects.all()
        for u in users_raw:
            bol = 0
            for fr in friend_request:
                a = fr.to_user == user and fr.from_user == u
                b = fr.to_user == u and fr.from_user == user
                if a or b:
                    bol = 1
                    break
            c = u in user.friends.all()
            if bol == 0 and (not c):
                users_r += [u]

    if request.method == "GET":
        return render(request, "base/nav-bar/index.html", { "games": game_list, "users": users_r})


## Vistas de login
def user_login(request): # Vista de la página de login
    if request.method == "GET":
       return render(request, "base/nav-bar/login.html")

    elif request.method == 'POST': # Si estamos recibiendo el form de registro
        # Tomar los elementos del formulario que vienen en request.POST
        username = request.POST['user']
        contraseña = request.POST['passw']

        # Autenticar al usuario
        user = authenticate(username=username, nombre=username, password=contraseña)

        if user is not None:
            # Redireccionar la página /home
            if user.is_active:
                # Guardar los datos de usuario
                login(request,user)
                user.last_login = timezone.now()
                user.save(update_fields=['last_login'])
                return HttpResponseRedirect('/home')
            else:
                # Esto no debiera pasar
                return HttpResponseRedirect('/add_game')
        else:
            # Redirigir a la misma página
            print("invalid login details " + username + " " + contraseña)
            return HttpResponseRedirect('/login')

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

def cuentaCreada(request): # Vista de la página de cuenta creada exitosamente
    new_user = request.POST["new-user"]
    new_password1 = request.POST["new-passw1"]
    new_password2 = request.POST["new-passw2"]

    # Se agrega el usuario a la base de datos
    user = User.objects.create_user(username=new_user, nombre=new_user, password=new_password1)
    users.update()

    user_media = UserMedia.objects.create(nombre="no",path="no",user=user)

    if request.method == "POST":
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
        return render(request, "base/resultados/cuenta-agregada.html", {"user": new_user})

def user_logout(request): # Vista de la página de logout
    logout(request)
    return render(request, "base/resultados/sesion-cerrada.html")
##


## Vistas de perfiles
def perfil(request): # Vista de la página del perfil del usuario activo
    this_user = request.user # Este usuario
    this_friend_requests = Friend_Request.objects.filter(to_user=this_user) # Filtra las solicitudes de amistad pendientes del usuario
    try:
        foto = UserMedia.objects.filter(user=this_user)[0] # Filtra la foto de este usuario
    except:
        foto = UserMedia.objects.filter(path="../../static/img/chinita.jpeg") # Arreglar

    this_reviews = Review.objects.filter(author=this_user) # Filtra las reseñas hechas por el usuario
    reviews = list(map(createReviewU, this_reviews))

    if request.method == "GET":
        return render(request, "base/perfil-usuario.html", {
            "reviews": reviews,
            "friend_requests": this_friend_requests,
            "user": request.user,
            "foto": foto,
            "users": users})

    elif request.method == "POST":
        return render(request, "base/perfil-usuario.html", {"reviews": reviews, "friend_requests": this_friend_requests, "user": request.user, "users": users})

def perfilPublico(request): # Vista de la página del perfil de un usuario en modo público
    user_search = request.GET["nombre"]
    that_user = User.objects.filter(id=user_search)[0]
    this_user = request.user

    if(that_user.id == this_user.id):
        return perfil(request)
    elif (this_user.is_anonymous):
        if request.method == "GET":
            that_foto = UserMedia.objects.filter(user=that_user)[0]
            return render(request, "base/perfil-publico.html", {
                "that_user": that_user,
                "foto": that_foto,
                "reviews": [],
                "friend_request": [],
                "bol": -1
                })
    else:
        fr = Friend_Request.objects.filter(Q(from_user=that_user)&Q(to_user=this_user))
        fr2 = Friend_Request.objects.filter(Q(from_user=this_user)&Q(to_user=that_user))
        that_foto = UserMedia.objects.filter(user=that_user)[0]
        if that_user in this_user.friends.all():
            bol = 1
            reviews = Review.objects.filter(author = that_user)
            reviews = list(map(createReviewU, reviews))
        else:
            bol = len(fr)*2
            reviews = []
            if bol > 0:
                fr = fr[0]
            else:
                bol = len(fr2)*3
        if request.method == "GET":
            return render(request, "base/perfil-publico.html", {
                "that_user": that_user,
                "foto": that_foto,
                "reviews": reviews,
                "friend_request": fr,
                "bol": bol
                })

def editar_perfil(request): # Vista de la página para editar el perfil del usuario
    if request.method == "GET":
        return render(request, "base/editar-perfil.html")

def perfil_actualizado(request): # Vista de la página de perfil actualizado exitosamente
    edit_edad = request.POST["edad"]
    edit_correo = request.POST["correo"]
    edit_descripcion_usuario = request.POST["descripcion_usuario"]
    foto = request.FILES["foto"]

    usuario = request.user
    usuario.edad = edit_edad
    usuario.email = edit_correo
    usuario.descripcion = edit_descripcion_usuario
    usuario.save(update_fields=["edad","email","descripcion"]) # Actualiza la información del usuario

    user_media = UserMedia.objects.filter(user=usuario)[0]

    # Se guarda la imagen con un nombre
    foto_name = foto.name
    hash_archivo = str(user_media.id) + hashlib.sha256(
            foto_name.encode()).hexdigest()[0:30]
    file_path = './base/static/user-media/' + hash_archivo
    with open(file_path, 'wb') as image:
        image.write(foto.file.read())

    user_media_path = user_media.path
    if (user_media_path != "no"):
        remove('./base/static/user-media/' + user_media_name)

    user_media.nombre = foto_name
    user_media.path  = hash_archivo
    user_media.save(update_fields=["nombre","path"])

    return redirect('perfil/')
##

## Vistas de amigos
@login_required
def send_friend_request(request, userID): # Vista para mandar una nueva solicitud de amistad
    from_user = request.user
    to_user = User.objects.get(id=userID)
    friend_request, created = Friend_Request.objects.get_or_create(from_user=from_user, to_user=to_user)
    if created:
        return render(request, "base/resultados/solicitud-enviada.html", {"user": from_user, "to_user": to_user})
    else:
        return render(request, "base/resultados/solicitud-errada.html", {"user": from_user, "to_user": to_user})

@login_required
def accept_friend_request(request, requestID): # Vista para aceptar una solicitud de amistad pendiente
    friend_request = Friend_Request.objects.get(id=requestID)
    this_user = friend_request.to_user
    that_user = friend_request.from_user
    if this_user == request.user:
        this_user.friends.add(that_user)
        that_user.friends.add(this_user)
        friend_request.delete()
        return render(request, "base/resultados/solicitud-aceptada.html", {"user": this_user, "to_user": that_user})
    else:
        return HttpResponse('friend request not accepted')
##


## Vistas de juegos
class GameL:
    # Clase que representa un objeto que contiene la información de un juego
    # que se va a mostrar en el listado de juegos
    def __init__(self):
        self.id = 0
        self.name = 0
        self.plataforma = 0
        self.genres = 0
        self.score = 0
        self.foto = 0

    def setAttributes(self, game):
        self.id = game.id
        self.name = game.nombre
        self.plataforma = game.plataforma
        self.genres = Genre.objects.filter(game=game)
        self.score = game.promedio
        self.foto = GameMedia.objects.filter(game=game)[0].path

def createGameL(game): # Función para crear un objeto de la clase GameL dado un juego
    gameL = GameL()
    gameL.setAttributes(game)
    return gameL


def popular_games(request): # Vista de la página del listado de juegos
    if request.method == "GET":
        # armar una lista que contienen objetos con la información necesaria
        # para mostrar listado de todos los juegos
        games = Game.objects.all() # Todos los juegos de la base de datos
        game_list = list(map(createGameL, games))

        return render(request, "base/nav-bar/popular-games.html", {"games": game_list})


def add_game(request): # Vista de la página de agregar nuevo juego
    if request.method == "GET":
        return render(request, "base/nav-bar/agregar-juego.html")

def juegoAgregado(request): # Vista de la página de juego agregado exitosamente
    nombre = request.POST["nombre"]
    anio = request.POST["anio"]
    descripcion = request.POST["descripcion"]
    desarrollador = request.POST["dev"]
    plat = request.POST["plat"]
    gen = request.POST.getlist("gen")
    foto = request.FILES["foto"]

    # Agrega el nuevo juego a la base de datos
    game = Game.objects.create(nombre=nombre, anio=anio, descripcion=descripcion, desarrollador=desarrollador, plataforma=plat, genero=gen)
    games.update()

    # Se agregan sus géneros a la base de datos
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

    # Registra los datos para mostrarlos
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

def perfilJuego(request): # Vista de la página del perfil de un juego
    if request.method == "GET":
        nombre = request.GET["nombre"]
        resultado = Game.objects.filter(id=nombre)
        if (len(resultado)==0):
            return render(request, "base/resultados/perfil-juego.html", {"bol": 0})

        reviews = Review.objects.filter(game=nombre)
        generos = Genre.objects.filter(game=nombre)
        foto = GameMedia.objects.filter(game=nombre)

        # Actualiza el promedio actual del juego según las reseñas
        try:
            prom = round(list(reviews.aggregate(Avg('score')).values())[0],1)
        except:
            # En caso de que no haya recibido reseñas todavía, muestra 0
            prom = 0.0
        resultado.update(promedio=prom) # Actualiza el promedio en los datos del juego

        return render(request, "base/resultados/perfil-juego.html", {
            "game": resultado[0],
            "reviews": reviews,
            "generos": generos,
            "foto": foto[0],
            "bol": 1,
            "prom": prom}
            )

def buscar(request): # Vista de la página de resultados de búsqueda
    buscado = request.GET["search"]
    # Filtra el nombre que se buscó en el nombre del juego, del desarrollador, y del género
    resultados = Game.objects.filter(Q(nombre__icontains=buscado) | Q(desarrollador__icontains=buscado) )
    resultados2 = Genre.objects.filter(Q(name__icontains=buscado))
    def getGame(genre):
        return genre.game

    def unionU(list1, list2):
        for e2 in list2:
            bol = 0
            for e1 in list1:
                if e1.id == e2.id:
                    bol = 1
                    continue 
            if bol==0:
                list1 += [e2]
        return list1 

    resultados2 = list(map(getGame, resultados2))

    resultados2 = list(map(createGameL, resultados2))
    resultados = list(map(createGameL, resultados))
    resultados = unionU(resultados, resultados2)
    

    if request.method == "GET":
        return render(request, "base/resultados/nombre-buscado.html", {"buscado": buscado, "resultados": resultados})
##

## Vistas de Reseñas
class ReviewU:
    # Clase que representa un objeto que contiene la información de una review
    # que se va a mostrar en el listado de reviews de un usuario
    def __init__(self):
        self.id_game = 0
        self.name_game = 0
        self.plataforma_game = 0
        self.foto= 0
        self.review_score = 0
        self.review_des = 0

    def setAttributes(self, review):
        game = review.game
        self.id_game = game.id
        self.name_game = game.nombre
        self.plataforma_game = game.plataforma
        self.foto = GameMedia.objects.filter(game=game)[0].path
        self.review_score = review.score
        self.review_des= review.body

def createReviewU(review): # Función para crear un objeto de la clase ReviewU dado una review
    reviewU= ReviewU()
    reviewU.setAttributes(review)
    return reviewU

def add_review(request): # Vista de la página para agregar reseñas
    if request.method == "GET":
        return render(request, "base/agregar-review.html", {"users" : users, "games": games})

def review_agregada(request): # Vista de la página de reseña agregada exitosamente
    autor = request.user
    juego = request.POST["game"]
    puntaje = request.POST["score"]
    review = request.POST["game_review"]

    if request.user.is_authenticated:
        # Deja al usuario activo como autor
        autor_user = User.objects.get(username=autor)
    else:
        # Deja un usuario anónimo como autor
        autor_user, created = User.objects.get_or_create(username="Anonimo", nombre = "Anonimo", password = "nada")
        if created:
            autor_user.save()

    juego_obj = Game.objects.get(nombre=juego)
    review = Review.objects.create(author=autor_user, game=juego_obj, score=puntaje, body=review) # Crea la reseña
    reviews.update() # Actualiza las reseñas en la base de datos

    game_reviews = reviews.filter(game=juego_obj)
    prom = round(list(game_reviews.aggregate(Avg('score')).values())[0],1) # Calcula el puntaje promedio
    thegame = games.filter(nombre=juego)
    thegame.update(promedio=prom) # Actualiza el puntaje promedio
    if request.method == "POST":
        review.save() # Guarda la reseña
        return render(request, "base/resultados/review-agregada.html", {"user": autor})
##
