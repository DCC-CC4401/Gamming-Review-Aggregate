from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
  path('home', views.home, name='home'), # Página principal

  # Urls de login
  path('login', views.user_login, name='user_login'),
  url(r'^login/validate_user_login/$', views.validate_user_login, name='validate_user_login/'),
  url(r'^login/validate_passw_login/$', views.validate_passw_login, name='validate_passw_login/'),
  url(r'^login/validate_username/$', views.validate_username, name='validate_username/'),
  url(r'^login/validate_password/$', views.validate_password, name='validate_password/'),
  url(r'^login/validate_both_passwords/$', views.validate_both_passwords, name='validate_both_passwords/'),
  path('cuenta-creada/', views.cuentaCreada, name='cuenta-creada/'),
  path('sesion_cerrada/', views.user_logout, name='sesion_cerrada/'),

  # Urls de perfiles
  path('perfil/', views.perfil, name='perfil/'),
  path('perfil_publico/', views.perfilPublico, name='perfil_publico/'),
  path('editar_perfil/', views.editar_perfil, name='editar_perfil/'),
  path('perfil_actualizado/', views.perfil_actualizado, name='perfil_actualizado/'),

  # Urls de amigos
  path('send_friend_request/<int:userID>/', views.send_friend_request, name='send friend request'),
  path('accept_friend_request/<int:requestID>/', views.accept_friend_request, name='accept friend request'),

  # Urls de juegos
  path('listado-juegos', views.popular_games, name='listado-juegos'),
  path('add_game', views.add_game, name='add_game'),
  path('juego-agregado/', views.juegoAgregado, name='juego-agregado/'),
  path('perfil-juego/', views.perfilJuego, name='perfil-juego/'),
  path('nombre-buscado/', views.buscar, name='nombre-buscado/'),

  # Urls de reseñas
  path('agregar_review/', views.add_review, name='agregar_review/'),
  path('review_agregada/', views.review_agregada, name='review_agregada/'),
]
