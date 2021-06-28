from django.contrib import admin
from base.models import User, Game, Review, Genre

# Esto es para poder ver los modelos al ingresar a localhost:8000/admin
# Se necesita crear un superusuario para administrar
# Comando: python manage.py createsuperuser
# Tomar en cuenta que esto hará que el super usuario inicie sesión en GRA, sobreescribiendo cualquier otra sesión previa
admin.site.register(User) # Para ver modelos de User
admin.site.register(Game) # Para ver modelos de Game
admin.site.register(Review) # Para ver modelos de Review
admin.site.register(Genre) # Para ver modelos de Genre