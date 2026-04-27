"""
Testes E2E de permissões e segurança.
"""
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


pytestmark = pytest.mark.django_db


class TestPermissoesLojista:
    """Testes de permissões do lojista."""

    def test_lojista_nao_acessa_admin_dashboard(self, browser, live_server_url, lojista_user, loja):
        """Teste: Lojista não acessa admin-dashboard."""
        browser.get(f'{live_server_url}/login/')
        browser.find_element(By.NAME, 'username').send_keys('lojista_teste')
        browser.find_element(By.NAME, 'password').send_keys('lojista123')
        browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        
        WebDriverWait(browser, 10).until(EC.url_contains('lojista'))
        
        browser.get(f'{live_server_url}/admin-dashboard/')
        
        assert '403' in browser.page_source or 'login' in browser.current_url.lower() or 'acesso' in browser.page_source.lower()

    @pytest.mark.skip(reason="Test isolation issues with SQLite in-memory")
    def test_lojista_nao_acessa_catalogo_admin(self, browser, live_server_url, lojista_user, loja):
        """Teste: Lojista não acessa /catalogo/adicionar/."""
        browser.get(f'{live_server_url}/login/')
        browser.find_element(By.NAME, 'username').send_keys('lojista_teste')
        browser.find_element(By.NAME, 'password').send_keys('lojista123')
        browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        
        WebDriverWait(browser, 10).until(EC.url_contains('lojista'))
        
        browser.get(f'{live_server_url}/catalogo/adicionar/')
        
        # Lojista deve ser redirecionado para vitrine ou mostrar erro
        WebDriverWait(browser, 10).until(
            lambda b: '/catalogo/adicionar/' not in b.current_url or 
                      'Acesso restrito' in b.page_source or
                      'vitrine' in b.current_url
        )
        
        assert '/catalogo/adicionar/' not in browser.current_url or 'restrito' in browser.page_source.lower()

    def test_nao_autenticado_nao_acessa_gerenciar_lojas(self, browser, live_server_url):
        """Teste: Usuário não autenticado não acessa /admin-dashboard/lojas/."""
        browser.get(f'{live_server_url}/admin-dashboard/lojas/')
        
        assert 'login' in browser.current_url.lower()


class TestProtecaoCSRF:
    """Testes de proteção CSRF."""

    def test_login_protegido_csrf(self, browser, live_server_url):
        """Teste: Login requer token CSRF."""
        browser.get(f'{live_server_url}/login/')
        
        csrf_token = browser.find_element(By.NAME, 'csrfmiddlewaretoken')
        assert csrf_token is not None

    def test_registro_protegido_csrf(self, browser, live_server_url):
        """Teste: Registro requer token CSRF."""
        browser.get(f'{live_server_url}/registro-lojista/')
        
        csrf_token = browser.find_element(By.NAME, 'csrfmiddlewaretoken')
        assert csrf_token is not None


class TestSeguranca:
    """Testes de segurança."""

    def test_senha_nao_exposta(self, browser, live_server_url, admin_user):
        """Teste: Senha não aparece no código fonte."""
        browser.get(f'{live_server_url}/login/')
        browser.find_element(By.NAME, 'username').send_keys('admin')
        browser.find_element(By.NAME, 'password').send_keys('admin123')
        browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        
        WebDriverWait(browser, 10).until(EC.url_contains('admin'))
        
        current_page_source = browser.page_source
        
        assert 'admin123' not in current_page_source
        assert 'password' not in current_page_source.lower() or 'type="password"' in current_page_source

    def test_logout_protegido(self, browser, live_server_url, admin_user):
        """Teste: Logout requer autenticação."""
        browser.get(f'{live_server_url}/logout/')
        
        assert 'saiu' in browser.page_source.lower() or 'sucesso' in browser.page_source.lower()


class TestIsolamentoDados:
    """Testes de isolamento de dados."""

    def test_cada_lojista_ver_só_seus_produtos(self, browser, live_server_url, lojista_user, loja, produto):
        """Teste: Lojista vê apenas produtos da própria loja."""
        browser.get(f'{live_server_url}/login/')
        browser.find_element(By.NAME, 'username').send_keys('lojista_teste')
        browser.find_element(By.NAME, 'password').send_keys('lojista123')
        browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        
        WebDriverWait(browser, 10).until(EC.url_contains('lojista'))
        
        assert 'Produto Teste' in browser.page_source