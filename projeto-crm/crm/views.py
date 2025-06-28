from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Produto
from decimal import Decimal
from django.contrib.messages import add_message, constants

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
            add_message(request, constants.ERROR, "Erro ao tentar cadastrar o produto!")
            return redirect('cadastro_produto')
        
        add_message(request, constants.SUCCESS, "Produto cadastrado com sucesso!")
        return redirect('cadastro_produto')
    
def editar_produto(request, id):
    if request.method == 'GET':
        produto = Produto.objects.get(id=id)
        return render(request, "produto_editar.html", {'produto': produto})
    
    if request.method == 'POST':
        produto = Produto.objects.get(id=id)

        try:
            produto.nome = request.POST.get('nome') if request.POST.get('nome') else produto.nome
            produto.descricao = request.POST.get('descricao') if request.POST.get('descricao') else produto.descricao
            produto.preco = request.POST.get('preco') if request.POST.get('preco') else produto.preco
            produto.qtd_estoque = request.POST.get('qtd_estoque') if request.POST.get('qtd_estoque') else produto.qtd_estoque
            produto.ativo = request.POST.get('ativo') if request.POST.get('ativo') else produto.ativo

            produto.save()
        except:
            add_message(request, constants.ERROR, "Erro ao tentar atualizar produto!")
            return redirect('cadastro_produto')
            
        add_message(request, constants.SUCCESS, "Produto atualizado com sucesso!")
        return redirect('cadastro_produto')