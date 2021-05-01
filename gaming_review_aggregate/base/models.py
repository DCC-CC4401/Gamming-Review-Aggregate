from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    nombre = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

#class Game(models.Model):
   # nombre = models.CharField(max_length=150)

#class Developer(models.Model):
   # nombre = models.CharField(max_length=150)

#class Rating(models.Model):
 #   puntaje = models.IntegerField(max_value=10, min_value=0) # esta wea la inventé

#class Review(models.Model):
   # body= models.CharField(max_length=5000)

#class Genre(models.Model):
    #nombre = models.CharField(max_length=30)


