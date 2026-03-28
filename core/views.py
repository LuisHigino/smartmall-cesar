from django.shortcuts import render
from .models import Produto 

def catalogo(request):
    produtos = Produto.objects.all()

    contexto = {
        'produtos': produtos
    }
    return render(request, 'core/catalogo.html', contexto)

