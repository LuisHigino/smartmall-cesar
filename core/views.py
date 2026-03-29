from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from .models import Produto, Loja
from .forms import ProdutoForm, LojaForm


def painel_catalogo(request):
    produtos = Produto.objects.all()
    return render(request, 'catalogo.html', {'produtos': produtos})


def home(request):
    return render(request, 'home.html')


@login_required
@user_passes_test(lambda u: u.is_staff)
def painel_lojas(request):
    lojas = Loja.objects.select_related('usuario').all()
    return render(request, 'lojas.html', {'lojas': lojas})


@login_required
@user_passes_test(lambda u: u.is_staff)
def cadastrar_loja(request):
    if request.method == 'POST':
        form = LojaForm(request.POST)
        if form.is_valid():
            loja = form.save(commit=False)
            cnpj = form.cleaned_data['cnpj']
            responsavel = form.cleaned_data['responsavel']

            username = cnpj.replace('.', '').replace('/', '').replace('-', '')
            senha_aleatoria = get_random_string(10)
            usuario_loja = User.objects.create_user(
                username=username,
                password=senha_aleatoria,
                first_name=responsavel,
                is_active=True,
            )
            loja.usuario = usuario_loja
            loja.save()
            messages.success(request, 'Loja cadastrada com sucesso')
            return redirect('painel_lojas')
    else:
        form = LojaForm()

    return render(request, 'cadastrar_loja.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.is_staff)
def editar_loja(request, id):
    loja = get_object_or_404(Loja, id=id)
    if request.method == 'POST':
        form = LojaForm(request.POST, instance=loja)
        if form.is_valid():
            form.save()
            messages.success(request, 'Loja atualizada com sucesso')
            return redirect('painel_lojas')
    else:
        form = LojaForm(instance=loja)
    return render(request, 'cadastrar_loja.html', {'form': form, 'acao': 'Editar'})


@login_required
@user_passes_test(lambda u: u.is_staff)
def remover_loja(request, id):
    loja = get_object_or_404(Loja, id=id)
    if request.method == 'POST':
        loja.delete()
        messages.success(request, 'Loja removida com sucesso')
        return redirect('painel_lojas')
    return render(request, 'remover_loja.html', {'loja': loja})


def adicionar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES) 
        if form.is_valid():
            form.save()
            return redirect('painel_catalogo')
    else:
        form = ProdutoForm()        
    contexto = {'form': form, 'acao': 'Adicionar'}
    return render(request, 'adicionar_produto.html', contexto)
    

def editar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
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
