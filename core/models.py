from django.db import models
from django.contrib.auth.models import User

class Produto(models.Model):
    nome = models.CharField('Nome', max_length=200)
    preco = models.DecimalField('Preco', max_digits=10, decimal_places=2)
    estoque = models.IntegerField('Estoque', default=0)
    descricao = models.TextField('Descrição', blank=True, null=True)
    imagem = models.ImageField('Imagem', upload_to='produtos/', blank=True, null=True)
    
    def __str__(self):
        return self.nome


class Loja(models.Model):
    nome = models.CharField('Nome da Loja', max_length=255)
    cnpj = models.CharField('CNPJ', max_length=18, unique=True)
    responsavel = models.CharField('Responsável', max_length=255)
    usuario = models.OneToOneField(User, on_delete=models.PROTECT, null=True, blank=True, related_name='loja')
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)

    def __str__(self):
        return self.nome


    
  





















