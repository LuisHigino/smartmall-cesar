from django.db import models

class Produto(models.Model):
    nome = models.CharField('Nome', max_lengt=200)
    preco = models.DecimalField('Preco', max_digits=10, decimal_places=2)
    estoque = models.IntegerField('Estoque', max_digits=1000000,)
    descricao = models.TextField('Descrição', blank=True, null=True)

    def __str__(self):
        return self.nome
    
  





















