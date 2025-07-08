from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.messages import add_message, constants
from django.contrib.auth.decorators import login_required


def cadastrar(request):
    if request.method == 'GET':
        return render(request, 'cadastrar_usuario.html')
    
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confir_senha = request.POST.get('confirmar_senha')

        if len(str(nome).strip()) < 6:
            add_message(request, constants.ERROR, "O nome de usuário deve conter no mínimo 6 caracteres")
            return redirect('cadastrar_usuario')

        if len(str(senha).strip()) < 8:
            add_message(request, constants.ERROR, "A senha deve conter no mínimo 8 caracteres")
            return redirect('cadastrar_usuario')
        
        if senha != confir_senha:
            add_message(request, constants.ERROR, "As senhas não são iguais!")
            return redirect('cadastrar_usuario')
        
        user = User.objects.filter(username=str(nome).strip().lower())

        if user.exists():
            add_message(request, constants.ERROR, "O nome de usuário já está sendo utilizado!")
            return redirect('cadastrar_usuario')
        
        try:
            User.objects.create_user(
                username=str(nome).strip().lower(),
                email=email,
                password=senha
            )
        except:
            add_message(request, constants.ERROR, "Erro ao tentar cadastrar o usuário!")
            return redirect('cadastrar_usuario')
        
        add_message(request, constants.SUCCESS, "Usuário cadastrado com sucesso!")
        return redirect('view_produtos')
        
