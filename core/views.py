from django.shortcuts import render, redirect, get_object_or_404
from .models import Produto 
from .models import ProdutoForm 



def painel_catalogo(request):
    produtos = Produto.objects.all()
    return render(request, 'catalogo.html', {'produtos': produtos})

def adicionar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adicionar_produto')
        else:
            form = ProdutoForm()
        
        contexto = {'form': form, 'acao': 'Adicionar'}
        return render(request, 'adicionar_produto.html', {'form': form})

def catalogo(request):
    produtos = Produto.objects.all()

    contexto = {
        'produtos': produtos
    }
    return render(request, 'core/catalogo.html', contexto)
