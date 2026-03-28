from django.shortcuts import render
from .models import Produto 
from .models import ProdutoForm 

def adicionar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adicionar_produto')
        else:
            form = ProdutoForm()

        return render(request, 'adicionar_produto.html', {'form': form})

def catalogo(request):
    produtos = Produto.objects.all()

    contexto = {
        'produtos': produtos
    }
    return render(request, 'core/catalogo.html', contexto)
