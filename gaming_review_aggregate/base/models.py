from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    nombre = models.CharField(max_length=30)
    password = models.CharField(max_length=30)