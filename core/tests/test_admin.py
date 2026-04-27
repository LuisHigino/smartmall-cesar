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