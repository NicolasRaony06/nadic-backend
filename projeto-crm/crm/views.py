from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Produto
from decimal import Decimal

def cadastro(request):
    if request.method == 'GET':
        return render(request, 'produto_cadastro.html')
    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        preco = request.POST.get('preco')
        qtd_estoque = request.POST.get('qtd_estoque')
        ativo = request.POST.get('ativo')

        try:
            produto = Produto.objects.create(
                nome = nome,
                descricao = descricao,
                preco = Decimal(preco),
                qtd_estoque = int(qtd_estoque),
                ativo = ativo
            )

            produto.save()
        except:
            print("Erro \n")
            return redirect('cadastro_produto')

        return redirect('cadastro_produto')
