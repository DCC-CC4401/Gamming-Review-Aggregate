from django.shortcuts import render, redirect
from django.http import HttpResponse


def home(request): #the homepage view
    if request.method == "GET":
       return render(request, "base/index.html")
