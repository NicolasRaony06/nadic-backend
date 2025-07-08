from django.shortcuts import render
from django.contrib import auth

def cadastrar(request):
    if request.method == 'GET':
        return render(request, 'cadastrar_usuario.html')
