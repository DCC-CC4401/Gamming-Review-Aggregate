from django.urls import path
from . import views

urlpatterns = [
  path('home', views.home, name='home'),
  path('login', views.login, name='login'),
  path('popular_games', views.popular_games, name='popular_games'),
]