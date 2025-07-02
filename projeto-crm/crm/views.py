from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Produto, Venda, ItemVenda
from decimal import Decimal
from django.contrib.messages import add_message, constants

def view_produtos(request):
    if request.method == 'GET':
        if request.GET.get('view_indisponivel'):
            produtos = Produto.objects.filter(ativo=False)
            return render(request, 'view_produtos.html', {'produtos': produtos})

        produtos = Produto.objects.filter(ativo=True)
        return render(request, 'view_produtos.html', {'produtos': produtos})

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
            return redirect('view_produtos')
        
        add_message(request, constants.SUCCESS, "Produto cadastrado com sucesso!")
        return redirect('view_produtos')
    
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
            return redirect('view_produtos')
            
        add_message(request, constants.SUCCESS, "Produto atualizado com sucesso!")
        return redirect('view_produtos')
    
def deletar_produto(request, id):
    if request.method == 'GET':
        try:
            produto = Produto.objects.get(id=id)
            produto.delete()
        except:
            add_message(request, constants.ERROR, "Erro ao tentar deletar produto!")
            return redirect('view_produtos')
        
        add_message(request, constants.SUCCESS, "Produto deletado com sucesso!")
        return redirect('view_produtos')
    
def comprar_produtos(request):
    if request.method == "POST":
        produtos = request.POST.getlist('produtos_selecionados')

        if len(produtos) < 1:
            add_message(request, constants.INFO, "Nenhum produto foi selecionado para a compra")
            return redirect('view_produtos')
    
        venda = Venda.objects.create()

        valor_total = 0
        for produto_id in produtos:
            try:
                produto = Produto.objects.get(id=int(produto_id))
                qtd_produto = request.POST[f'quantidade_{produto_id}']

                item = ItemVenda.objects.create(
                    venda=venda,
                    produto=produto,
                    qtd_produto=int(qtd_produto),
                    preco_und=produto.preco
                )

                produto.qtd_estoque -= int(qtd_produto)

                if produto.qtd_estoque < 1:
                    produto.ativo = False
                
                produto.save()

                valor_total += item.subtotal()

                item.save()
            except:
                add_message(request, constants.ERROR, f"Falha no registro de compra do produto {produto_id}")
                return redirect('view_produtos')
            
        try:
            venda.valor_total = valor_total
            venda.save()
        except:
            add_message(request, constants.ERROR, f"Falha na tentativa de compra!")
            return redirect('view_produtos')

        add_message(request, constants.SUCCESS, "Produto comprado com sucesso!")
        return redirect('view_produtos')