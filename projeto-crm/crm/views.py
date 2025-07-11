from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Produto, Venda, ItemVenda, is_superuser
from decimal import Decimal
from django.contrib.messages import add_message, constants
from django.contrib.auth.decorators import login_required

def view_produtos(request):
    produtos = Produto.objects.all()
    if request.method == 'GET':
        filtro = request.GET.get('filter')
        search_input = request.GET.get('search-input')
        try: 
            if filtro and search_input:
                if filtro == 'name':
                    produtos = produtos.filter(nome__icontains=search_input)
                elif filtro == 'preco':
                    produtos = produtos.filter(preco=Decimal(search_input))
        except:
            add_message(request, constants.ERROR, "Erro ao tentar filtrar o produto!")
            return redirect('view_produtos')

        if request.GET.get('view_indisponivel') and is_superuser(request):
            return render(request, 'view_produtos.html', {'produtos': produtos.filter(ativo=False)})

        return render(request, 'view_produtos.html', {'produtos': produtos.filter(ativo=True)})

@login_required(login_url="login")
def cadastro(request):
    if not is_superuser(request):
        add_message(request, constants.WARNING, "Você não tem acesso para isso!")
        return redirect('view_produtos')

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

@login_required(login_url="login")  
def editar_produto(request, id):
    if not is_superuser(request):
        add_message(request, constants.WARNING, "Você não tem acesso para isso!")
        return redirect('view_produtos')
    
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

@login_required(login_url="login") 
def deletar_produto(request, id):
    if not is_superuser(request):
        add_message(request, constants.WARNING, "Você não tem acesso para isso!")
        return redirect('view_produtos')
    
    if request.method == 'GET':
        try:
            produto = Produto.objects.get(id=id)
            produto.delete()
        except:
            add_message(request, constants.ERROR, "Erro ao tentar deletar produto!")
            return redirect('view_produtos')
        
        add_message(request, constants.SUCCESS, "Produto deletado com sucesso!")
        return redirect('view_produtos')

@login_required(login_url="login") 
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

@login_required(login_url="login")
def dashboard_produtos(request):
    if not is_superuser(request):
        add_message(request, constants.WARNING, "Você não tem acesso para isso!")
        return redirect('view_produtos')
    
    if request.method == 'GET':
        vendas = Venda.objects.all()

        faturamento = 0
        for venda in vendas:
            faturamento += venda.valor_total

        produtos = Produto.objects.all()
        faturamento_per_produto = []
        estoque_total = 0
        for produto in produtos:
            estoque_total += produto.qtd_estoque
            valor_total = 0
            for item in ItemVenda.objects.filter(produto=produto):
                valor_total += item.subtotal()

            if valor_total > 0:
                faturamento_per_produto.append((produto.nome, produto.preco, valor_total))

        return render(request, 'dashboard_produtos.html', {'faturamento':faturamento, 'faturamento_per_produto': faturamento_per_produto, 'vendas': vendas, 'produtos': produtos, 'estoque_total': estoque_total})
