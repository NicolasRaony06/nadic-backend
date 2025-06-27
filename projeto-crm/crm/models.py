from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=50)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    qtd_estoque = models.IntegerField()
    ativo = models.BooleanField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome

class Venda(models.Model):
    data_venda = models.DateTimeField(auto_now_add=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    produtos = models.ManyToManyField(Produto, through='ItemVenda')

    def __str__(self):
        return f"{self.data_venda},{self.valor_total}"
    
class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    qtd_produto = models.IntegerField()
    preco_und = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.preco_und * self.qtd_produto

    def __str__(self):
        return f"{self.produto.nome},{self.preco_und}"  