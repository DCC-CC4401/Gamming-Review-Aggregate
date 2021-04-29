from django.shortcuts import render, redirect
from django.http import HttpResponse


def home(request): #the homepage view
    if request.method == "GET":
       return render(request, "base/index.html")

def login(request): #the login view
    if request.method == "GET":
       return render(request, "base/login.html")

def popular_games(request): #the login view
    if request.method == "GET":
       return render(request, "base/popular-games.html")
