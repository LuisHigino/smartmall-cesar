"""
Configurações e fixtures para testes E2E com Selenium.
"""
import pytest
from django.contrib.auth.models import User

from core.models import Categoria, Loja, Produto


@pytest.fixture(scope='function', autouse=True)
def _setup_db(db):
    """Limpa o banco de dados antes de cada teste."""
    pass


@pytest.fixture(scope='function')
def browser():
    """Cria o driver do Selenium para cada teste."""
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.fixture(scope='function')
def live_server_url(live_server):
    """URL do servidor de teste."""
    return live_server.url


@pytest.fixture
def admin_user(db):
    """Cria usuário administrador."""
    User.objects.filter(username='admin').delete()
    user = User.objects.create_user(
        username='admin',
        email='admin@teste.com',
        password='admin123',
        is_staff=True,
        is_superuser=True
    )
    return user


@pytest.fixture
def lojista_user(db):
    """Cria usuário lojista."""
    User.objects.filter(username='lojista_teste').delete()
    return User.objects.create_user(
        username='lojista_teste',
        email='lojista@teste.com',
        password='lojista123'
    )


@pytest.fixture
def categoria(db):
    """Cria uma categoria para testes."""
    Categoria.objects.filter(nome='Restaurantes').delete()
    return Categoria.objects.create(nome='Restaurantes')


@pytest.fixture
def categoria_lojas(db):
    """Cria uma categoria para lojas."""
    Categoria.objects.filter(nome='Lojas').delete()
    return Categoria.objects.create(nome='Lojas')


@pytest.fixture
def categoria_informatica(db):
    """Cria categoria de informática."""
    Categoria.objects.filter(nome='Informática').delete()
    return Categoria.objects.create(nome='Informática')


@pytest.fixture
def loja(db, lojista_user, categoria):
    """Cria uma loja para testes."""
    Loja.objects.filter(cnpj='12.345.678/0001-90').delete()
    return Loja.objects.create(
        nome='Loja Teste',
        cnpj='12.345.678/0001-90',
        responsavel='João Silva',
        usuario=lojista_user,
        categoria=categoria
    )


@pytest.fixture
def produto(db, loja):
    """Cria um produto para testes."""
    Produto.objects.filter(nome='Produto Teste').delete()
    return Produto.objects.create(
        nome='Produto Teste',
        preco=99.99,
        estoque=10,
        loja=loja
    )


@pytest.fixture
def produto_estoque_baixo(db, loja):
    """Cria um produto com estoque baixo."""
    Produto.objects.filter(nome='Produto Estoque Baixo').delete()
    return Produto.objects.create(
        nome='Produto Estoque Baixo',
        preco=49.99,
        estoque=3,
        loja=loja
    )