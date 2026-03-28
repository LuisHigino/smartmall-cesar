from django.db import models

class Produto(models.Model):
    nome = models.CharField('Nome', max_length=200)
    preco = models.DecimalField('Preco', max_digits=10, decimal_places=2)
    estoque = models.IntegerField('Estoque', default=0)
    descricao = models.TextField('Descrição', blank=True, null=True)

    def __str__(self):
        return self.nome
    
  





















