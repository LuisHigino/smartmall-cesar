from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.views import LoginView
from django.utils.crypto import get_random_string

from .models import Produto, Loja, Categoria
from .forms import ProdutoForm, LojaForm, LojistaRegistrationForm


class CustomLoginView(LoginView):
    def get_success_url(self):
        if self.request.user.is_staff:
            return '/admin-dashboard/'
        elif hasattr(self.request.user, 'loja'):
            return '/lojista/'
        return '/vitrine/'


def logout_view(request):
    from django.contrib.auth import logout as auth_logout
    auth_logout(request)
    return render(request, 'registration/logout.html')


def painel_catalogo(request):
    produtos = Produto.objects.all()
    return render(request, 'catalogo.html', {'produtos': produtos})


def home(request):
    # Opção A: a home vira um redirect para a vitrine (perspectiva do cliente)
    return redirect('vitrine')


def vitrine(request):
    """
    Vitrine pública de lojas, com filtro por categoria (?categoria=<id>).
    """
    categorias = Categoria.objects.all()
    categoria_id = request.GET.get('categoria')

    lojas = Loja.objects.select_related('categoria').all()
    if categoria_id:
        lojas = lojas.filter(categoria_id=categoria_id)

    return render(request, 'vitrine.html', {
        'categorias': categorias,
        'lojas': lojas,
    })


@login_required
@user_passes_test(lambda u: u.is_staff)
def painel_lojas(request):
    lojas = Loja.objects.select_related('usuario', 'categoria').all()
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
    if not request.user.is_staff:
        messages.error(request, 'Acesso restrito a administradores.')
        return redirect('vitrine')
    
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
    if not request.user.is_staff:
        messages.error(request, 'Acesso restrito a administradores.')
        return redirect('vitrine')
    
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
    if not request.user.is_staff:
        messages.error(request, 'Acesso restrito a administradores.')
        return redirect('vitrine')
    
    produto = get_object_or_404(Produto, id=id)
    if request.method == 'POST':
        produto.delete()
        return redirect('painel_catalogo')

    return render(request, 'remover_produto.html', {'produto': produto})


def registrar_lojista(request):
    if request.method == 'POST':
        form = LojistaRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Loja cadastrada com sucesso! Bem-vindo, {username}.')
            # Faz login automaticamente após o registro
            auth_login(request, user)
            return redirect('lojista_dashboard')
    else:
        form = LojistaRegistrationForm()
    
    return render(request, 'registro_lojista.html', {'form': form})


@login_required
def lojista_dashboard(request):
    # Verifica se o usuário tem uma loja associada
    if not hasattr(request.user, 'loja'):
        messages.error(request, 'Você não tem uma loja associada. Contate o administrador.')
        return redirect('vitrine')
    
    loja = request.user.loja
    produtos = loja.produtos.all()
    
    context = {
        'loja': loja,
        'produtos': produtos,
        'total_produtos': produtos.count(),
        'estoque_baixo': produtos.filter(estoque__lt=5).count(),
    }
    
    return render(request, 'lojista_dashboard.html', context)


@login_required
def lojista_editar_perfil(request):
    if not hasattr(request.user, 'loja'):
        messages.error(request, 'Você não tem uma loja associada. Contate o administrador.')
        return redirect('vitrine')
    
    loja = request.user.loja
    
    if request.method == 'POST':
        form = LojaForm(request.POST, instance=loja)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil da loja atualizado com sucesso!')
            return redirect('lojista_dashboard')
    else:
        form = LojaForm(instance=loja)
    
    return render(request, 'lojista_editar_perfil.html', {'form': form, 'loja': loja})


@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    total_lojas = Loja.objects.count()
    total_produtos = Produto.objects.count()
    total_categorias = Categoria.objects.count()
    
    # Lojistas recentes (últimos 5)
    lojas_recentes = Loja.objects.select_related('usuario', 'categoria').order_by('-criado_em')[:5]
    
    context = {
        'total_lojas': total_lojas,
        'total_produtos': total_produtos,
        'total_categorias': total_categorias,
        'lojas_recentes': lojas_recentes,
    }
    
    return render(request, 'admin_dashboard.html', context)


@login_required
@user_passes_test(lambda u: u.is_staff)
def gerenciar_lojas(request):
    lojas = Loja.objects.select_related('usuario', 'categoria').all()
    return render(request, 'gerenciar_lojas.html', {'lojas': lojas})


@login_required
def lojista_adicionar_produto(request):
    if not hasattr(request.user, 'loja'):
        messages.error(request, 'Você não tem uma loja associada.')
        return redirect('vitrine')
    
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            produto = form.save(commit=False)
            produto.loja = request.user.loja
            produto.save()
            messages.success(request, 'Produto cadastrado com sucesso!')
            return redirect('lojista_dashboard')
    else:
        form = ProdutoForm()
    
    return render(request, 'lojista_produto_form.html', {'form': form, 'acao': 'Adicionar'})


@login_required
def lojista_editar_produto(request, id):
    if not hasattr(request.user, 'loja'):
        messages.error(request, 'Você não tem uma loja associada.')
        return redirect('vitrine')
    
    produto = get_object_or_404(Produto, id=id, loja=request.user.loja)
    
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto atualizado com sucesso!')
            return redirect('lojista_dashboard')
    else:
        form = ProdutoForm(instance=produto)
    
    return render(request, 'lojista_produto_form.html', {'form': form, 'acao': 'Editar'})


@login_required
def lojista_remover_produto(request, id):
    if not hasattr(request.user, 'loja'):
        messages.error(request, 'Você não tem uma loja associada.')
        return redirect('vitrine')
    
    produto = get_object_or_404(Produto, id=id, loja=request.user.loja)
    
    if request.method == 'POST':
        produto.delete()
        messages.success(request, 'Produto removido com sucesso!')
        return redirect('lojista_dashboard')
    
    return render(request, 'lojista_produto_confirm_delete.html', {'produto': produto})


def detalhe_loja(request, loja_id):
    loja = get_object_or_404(Loja, id=loja_id)
    produtos = Produto.objects.filter(loja=loja)

    return render(request, 'detalhe_loja.html', {
        'loja': loja,
        'produtos': produtos
     })