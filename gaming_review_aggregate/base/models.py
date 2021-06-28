from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser): # Clase para usuarios, con toda su información personal
    nombre = models.CharField(max_length=30, default="user")
    password = models.CharField(blank=False, max_length=100)
    edad = models.IntegerField(null=True)
    descripcion = models.TextField(max_length=2000, default="Acá va la descripción de usuario")
    friends = models.ManyToManyField("User", blank=True)


class Game(models.Model): # Clase para juegos, con todas sus especificaciones
    nombre = models.CharField(max_length=150)
    anio = models.IntegerField()
    descripcion = models.TextField(max_length=2000)
    desarrollador = models.CharField(max_length=150)
    genero = models.CharField(max_length=150)
    plataforma = models.CharField(max_length=150, default="PC")
    promedio = models.FloatField(default=0)


class Genre(models.Model): # Clase para los géneros de los juegos
    name = models.CharField(max_length=30)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)


class Friend_Request(models.Model): # Clase para las solicitudes de amistad
   from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
   to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)


class Review(models.Model): # Clase para las reseñas, con sus respectivas llaves foráneas y atributos
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    body = models.TextField(max_length= 2000, blank=True)


class GameMedia(models.Model): # Clase para las imágenes de los juegos
    nombre = models.CharField(max_length=150)
    path = models.CharField(max_length=150)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)


class UserMedia(models.Model): # Clase para las imágenes de los usuarios
    nombre = models.CharField(max_length=150)
    path = models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


