from django.shortcuts import render
from .models import Categoria, Loja

def shopping_view(request):
    categorias = Categoria.objects.all()
    
    categoria_id = request.GET.get('categoria')
    
    if categoria_id:
        lojas = Loja.objects.filter(categoria_id=categoria_id)
    else:
        lojas = Loja.objects.all()
    
    return render(request, 'vitrine.html', {
        'categorias': categorias,
        'lojas': lojas
    })