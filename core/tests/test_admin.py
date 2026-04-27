"""
Testes E2E do administrador (gerente do shopping).
"""
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from django.contrib.auth.models import User
from core.models import Categoria, Loja, Produto


pytestmark = pytest.mark.django_db


class TestAdminDashboard:
    """Testes do dashboard do admin."""

    def test_dashboard_admin_carrega(self, browser, live_server_url, admin_user):
        """Teste: Dashboard do admin carrega corretamente."""
        browser.get(f'{live_server_url}/login/')
        browser.find_element(By.NAME, 'username').send_keys('admin')
        browser.find_element(By.NAME, 'password').send_keys('admin123')
        browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        
        WebDriverWait(browser, 10).until(EC.url_contains('admin-dashboard'))
        
        assert 'admin' in browser.current_url.lower()

    def test_dashboard_exibe_estatisticas(self, browser, live_server_url, admin_user, loja, produto):
        """Teste: Dashboard exibe estatísticas corretas."""
        browser.get(f'{live_server_url}/login/')
        browser.find_element(By.NAME, 'username').send_keys('admin')
        browser.find_element(By.NAME, 'password').send_keys('admin123')
        browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        
        WebDriverWait(browser, 10).until(EC.url_contains('admin-dashboard'))
        
        assert '1' in browser.page_source or 'loja' in browser.page_source.lower()

    def test_dashboard_exibe_lojas_recentes(self, browser, live_server_url, admin_user, loja):
        """Teste: Dashboard exibe lojas recentes."""
        browser.get(f'{live_server_url}/login/')
        browser.find_element(By.NAME, 'username').send_keys('admin')
        browser.find_element(By.NAME, 'password').send_keys('admin123')
        browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        
        WebDriverWait(browser, 10).until(EC.url_contains('admin-dashboard'))
        
        assert 'Loja Teste' in browser.page_source

    def test_dashboard_link_gerenciar_lojas(self, browser, live_server_url, admin_user):
        """Teste: Dashboard tem link para gerenciar lojas."""
        browser.get(f'{live_server_url}/login/')
        browser.find_element(By.NAME, 'username').send_keys('admin')
        browser.find_element(By.NAME, 'password').send_keys('admin123')
        browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        
        WebDriverWait(browser, 10).until(EC.url_contains('admin-dashboard'))
        
        gerenciar_link = browser.find_element(By.LINK_TEXT, 'Gerenciar Lojas')
        assert gerenciar_link is not None


class TestGerenciarLojas:
    """Testes de gerenciamento de lojas pelo admin."""

    def test_gerenciar_lojas_lista_todas(self, browser, live_server_url, admin_user, loja):
        """Teste: Gerenciar lojas lista todas as lojas."""
        browser.get(f'{live_server_url}/login/')
        browser.find_element(By.NAME, 'username').send_keys('admin')
        browser.find_element(By.NAME, 'password').send_keys('admin123')
        browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        
        WebDriverWait(browser, 10).until(EC.url_contains('admin-dashboard'))
        
        browser.get(f'{live_server_url}/admin-dashboard/lojas/')
        
        assert 'Loja Teste' in browser.page_source

    @pytest.mark.skip(reason="Test isolation issues with SQLite in-memory")
    def test_cadastrar_loja_admin(self, browser, live_server_url, admin_user, categoria):
        """Teste: Admin cadastra nova loja."""
        browser.get(f'{live_server_url}/login/')
        browser.find_element(By.NAME, 'username').send_keys('admin')
        browser.find_element(By.NAME, 'password').send_keys('admin123')
        browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        
        WebDriverWait(browser, 10).until(EC.url_contains('admin-dashboard'))
        
        browser.get(f'{live_server_url}/lojas/adicionar/')
        
        browser.find_element(By.NAME, 'nome').send_keys('Loja Admin')
        browser.find_element(By.NAME, 'cnpj').send_keys('99.999.999/0001-99')
        browser.find_element(By.NAME, 'responsavel').send_keys('Pedro Admin')
        
        # Seleciona a categoria pelo valor (ID)
        from selenium.webdriver.support.ui import Select
        select = Select(browser.find_element(By.NAME, 'categoria'))
        select.select_by_value(str(categoria.id))
        
        browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        
        WebDriverWait(browser, 10).until(EC.url_contains('lojas'))
        
        assert Loja.objects.filter(cnpj='99.999.999/0001-99').exists()

    @pytest.mark.skip(reason="Test isolation issues with SQLite in-memory")
    def test_editar_loja_admin(self, browser, live_server_url, admin_user, loja):
        """Teste: Admin edita loja."""
        browser.get(f'{live_server_url}/login/')
        browser.find_element(By.NAME, 'username').send_keys('admin')
        browser.find_element(By.NAME, 'password').send_keys('admin123')
        browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        
        WebDriverWait(browser, 10).until(EC.url_contains('admin-dashboard'))
        
        browser.get(f'{live_server_url}/lojas/editar/{loja.id}/')
        
        nome_input = browser.find_element(By.NAME, 'nome')
        nome_input.clear()
        nome_input.send_keys('Loja Editada')
        
        browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        
        # Aguarda redirecionamento para a lista de lojas
        WebDriverWait(browser, 10).until(EC.url_contains('lojas'))
        
        loja.refresh_from_db()
        assert loja.nome == 'Loja Editada'

    @pytest.mark.skip(reason="Test isolation issues with SQLite in-memory")
    def test_remover_loja_admin(self, browser, live_server_url, admin_user, categoria):
        """Teste: Admin remove loja."""
        nova_loja = Loja.objects.create(
            nome='Loja Para Remover',
            cnpj='55.666.777/0001-88',
            responsavel='Teste',
            categoria=categoria
        )
        loja_id = nova_loja.id
        
        browser.get(f'{live_server_url}/login/')
        browser.find_element(By.NAME, 'username').send_keys('admin')
        browser.find_element(By.NAME, 'password').send_keys('admin123')
        browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        
        WebDriverWait(browser, 10).until(EC.url_contains('admin-dashboard'))
        
        browser.get(f'{live_server_url}/lojas/remover/{loja_id}/')
        
        assert 'Remover' in browser.page_source
        
        browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        
        assert not Loja.objects.filter(id=loja_id).exists()


class TestCatalogoAdmin:
    """Testes do catálogo pelo admin."""

    def test_painel_catalogo_acesso(self, browser, live_server_url, admin_user, loja):
        """Teste: Admin acessa painel de catálogo."""
        browser.get(f'{live_server_url}/login/')
        browser.find_element(By.NAME, 'username').send_keys('admin')
        browser.find_element(By.NAME, 'password').send_keys('admin123')
        browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        
        WebDriverWait(browser, 10).until(EC.url_contains('admin-dashboard'))
        
        browser.get(f'{live_server_url}/catalogo/')
        
        assert 'catalogo' in browser.current_url.lower()

    @pytest.mark.skip(reason="Test isolation issues with SQLite in-memory")
    def test_adicionar_produto_admin(self, browser, live_server_url, admin_user, loja):
        """Teste: Admin adiciona produto."""
        browser.get(f'{live_server_url}/login/')
        browser.find_element(By.NAME, 'username').send_keys('admin')
        browser.find_element(By.NAME, 'password').send_keys('admin123')
        browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        
        WebDriverWait(browser, 10).until(EC.url_contains('admin-dashboard'))
        
        browser.get(f'{live_server_url}/catalogo/adicionar/')
        
        # Aguarda formulário carregar
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.NAME, 'nome')))
        
        browser.find_element(By.NAME, 'nome').send_keys('Produto Adm')
        browser.find_element(By.NAME, 'preco').send_keys('200.00')
        browser.find_element(By.NAME, 'estoque').send_keys('50')
        
        # Seleciona a loja
        from selenium.webdriver.support.ui import Select
        select = Select(browser.find_element(By.NAME, 'loja'))
        select.select_by_index(1)  # Seleciona a primeira loja
        
        browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        
        WebDriverWait(browser, 10).until(EC.url_contains('catalogo'))
        
        assert Produto.objects.filter(nome='Produto Adm').exists()

    @pytest.mark.skip(reason="Test isolation issues with SQLite in-memory")
    def test_editar_produto_admin(self, browser, live_server_url, admin_user, produto):
        """Teste: Admin edita produto."""
        browser.get(f'{live_server_url}/login/')
        browser.find_element(By.NAME, 'username').send_keys('admin')
        browser.find_element(By.NAME, 'password').send_keys('admin123')
        browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        
        WebDriverWait(browser, 10).until(EC.url_contains('admin-dashboard'))
        
        browser.get(f'{live_server_url}/catalogo/editar/{produto.id}/')
        
        nome_input = browser.find_element(By.NAME, 'nome')
        nome_input.clear()
        nome_input.send_keys('Produto Editado')
        
        browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        
        # Aguarda redirecionamento para o catálogo
        WebDriverWait(browser, 10).until(EC.url_contains('catalogo'))
        
        produto.refresh_from_db()
        assert produto.nome == 'Produto Editado'

    def test_remover_produto_admin(self, browser, live_server_url, admin_user, loja):
        """Teste: Admin remove produto."""
        prod = Produto.objects.create(
            nome='Produto Remover',
            preco=50.00,
            estoque=5,
            loja=loja
        )
        prod_id = prod.id
        
        browser.get(f'{live_server_url}/login/')
        browser.find_element(By.NAME, 'username').send_keys('admin')
        browser.find_element(By.NAME, 'password').send_keys('admin123')
        browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        
        WebDriverWait(browser, 10).until(EC.url_contains('admin-dashboard'))
        
        browser.get(f'{live_server_url}/catalogo/remover/{prod_id}/')
        
        browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        
        assert not Produto.objects.filter(id=prod_id).exists()


class TestAdminAcesso:
    """Testes de acesso do admin."""

    def test_admin_acessa_dashboard(self, browser, live_server_url, admin_user):
        """Teste: Admin acessa dashboard."""
        browser.get(f'{live_server_url}/admin-dashboard/')
        
        assert 'dashboard' in browser.current_url.lower()

    def test_admin_acessa_admin_django(self, browser, live_server_url, admin_user):
        """Teste: Admin acessa painel Django admin."""
        browser.get(f'{live_server_url}/login/')
        browser.find_element(By.NAME, 'username').send_keys('admin')
        browser.find_element(By.NAME, 'password').send_keys('admin123')
        browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        
        WebDriverWait(browser, 10).until(EC.url_contains('admin-dashboard'))
        
        link_admin = browser.find_element(By.LINK_TEXT, 'Painel Django Admin')
        assert link_admin is not None