from django.shortcuts import render, redirect, get_object_or_404
from .models import Produto 
from .forms import ProdutoForm 

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
    return render(request, 'adicionar_produto.html', contexto)

def editar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('painel_catalogo')
    else:
        form = ProdutoForm(instance=produto)           

    contexto = {'form': form, 'acao': 'Editar'}
    return render(request, 'adicionar_produto.html', contexto)

def remover_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    if request.method == 'POST':
        produto.delete()
        return redirect('painel_catalogo')
    
    return render(request, 'remover_produto.html', {'produto': produto})


