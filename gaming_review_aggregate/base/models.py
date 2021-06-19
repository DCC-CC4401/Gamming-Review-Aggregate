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


class Platform(models.Model):
    name = models.CharField(max_length=150)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)


class Genre(models.Model):
    name = models.CharField(max_length=30)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)


class Rating(models.Model):
    #score = models.IntegerField(max_value=10, min_value=0)  # nose si existen min y max value
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
    review_body = models.TextField(max_length=2000)


#class Friendship(models.Model):
#   user1 = models.ForeignKey(User, on_delete=models.CASCADE)
#   user2 = models.ForeignKey(User, on_delete=models.CASCADE)

class Friend_Request(models.Model):
   from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
   to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)


class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    body = models.TextField(max_length= 2000)

#class GameMedia(models.Model):
   #img = models.image??? ayuda
   #game = models.ForeignKey(Game, on_delete=models.CASCADE)

#class UserMedia(models.Model):
  #user = models.ForeignKey(User, on_delete=models.CASCADE)


