from django.urls import path
from . import views

urlpatterns = [
  path('home', views.home, name='home'),
  path('login', views.login, name='login'),
  path('popular_games', views.popular_games, name='popular_games'),
  path('add_game', views.add_game, name='add_game'),
  path('nombre-buscado/', views.buscar, name='nombre-buscado/'),
  path('juego-agregado/', views.juegoAgregado, name='juego-agregado/'),
  path('cuenta-creada/', views.cuentaCreada, name='cuenta-creada/'),
]