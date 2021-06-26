from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    nombre = models.CharField(max_length=30, default="user")
    password = models.CharField(blank=False, max_length=100)
    edad = models.IntegerField(null=True)
    descripcion = models.TextField(max_length=2000, default="Acá va la descripción de usuario")
    friends = models.ManyToManyField("User", blank=True)


class Game(models.Model):
    nombre = models.CharField(max_length=150)
    anio = models.IntegerField()
    descripcion = models.TextField(max_length=2000)
    desarrollador = models.CharField(max_length=150)
    genero = models.CharField(max_length=150)
    plataforma = models.CharField(max_length=150, default="PC")
    promedio = models.FloatField(default=0)


class Platform(models.Model):
    name = models.CharField(max_length=150)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)


class Genre(models.Model):
    name = models.CharField(max_length=30)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)


class Friend_Request(models.Model):
   from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
   to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)


class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    body = models.TextField(max_length= 2000, blank=True)

#class GameMedia(models.Model):
   #img = models.image??? ayuda
   #game = models.ForeignKey(Game, on_delete=models.CASCADE)

#class UserMedia(models.Model):
  #user = models.ForeignKey(User, on_delete=models.CASCADE)


