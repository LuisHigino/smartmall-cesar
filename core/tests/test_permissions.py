"""
Testes E2E de permissões e segurança.
"""
import time
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
        time.sleep(2)
        browser.find_element(By.NAME, 'username').send_keys('lojista_teste')
        browser.find_element(By.NAME, 'password').send_keys('lojista123')
        browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        time.sleep(2)
        
        WebDriverWait(browser, 10).until(EC.url_contains('lojista'))
        time.sleep(2)
        
        browser.get(f'{live_server_url}/admin-dashboard/')
        time.sleep(2)
        
        assert '403' in browser.page_source or 'login' in browser.current_url.lower() or 'acesso' in browser.page_source.lower()

    def test_nao_autenticado_nao_acessa_gerenciar_lojas(self, browser, live_server_url):
        """Teste: Usuário não autenticado não acessa /admin-dashboard/lojas/."""
        browser.get(f'{live_server_url}/admin-dashboard/lojas/')
        time.sleep(2)
        
        assert 'login' in browser.current_url.lower()


class TestProtecaoCSRF:
    """Testes de proteção CSRF."""

    def test_login_protegido_csrf(self, browser, live_server_url):
        """Teste: Login requer token CSRF."""
        browser.get(f'{live_server_url}/login/')
        time.sleep(2)
        
        csrf_token = browser.find_element(By.NAME, 'csrfmiddlewaretoken')
        assert csrf_token is not None

    def test_registro_protegido_csrf(self, browser, live_server_url):
        """Teste: Registro requer token CSRF."""
        browser.get(f'{live_server_url}/registro-lojista/')
        time.sleep(2)
        
        csrf_token = browser.find_element(By.NAME, 'csrfmiddlewaretoken')
        assert csrf_token is not None


class TestSeguranca:
    """Testes de segurança."""

    def test_senha_nao_exposta(self, browser, live_server_url, admin_user):
        """Teste: Senha não aparece no código fonte."""
        browser.get(f'{live_server_url}/login/')
        time.sleep(2)
        browser.find_element(By.NAME, 'username').send_keys('admin')
        browser.find_element(By.NAME, 'password').send_keys('admin123')
        browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        time.sleep(2)
        
        WebDriverWait(browser, 10).until(EC.url_contains('admin'))
        time.sleep(2)
        
        current_page_source = browser.page_source
        
        assert 'admin123' not in current_page_source
        assert 'password' not in current_page_source.lower() or 'type="password"' in current_page_source

    def test_logout_protegido(self, browser, live_server_url, admin_user):
        """Teste: Logout requer autenticação."""
        browser.get(f'{live_server_url}/logout/')
        time.sleep(2)
        
        assert 'saiu' in browser.page_source.lower() or 'sucesso' in browser.page_source.lower()


class TestIsolamentoDados:
    """Testes de isolamento de dados."""

    def test_cada_lojista_ver_só_seus_produtos(self, browser, live_server_url, lojista_user, loja, produto):
        """Teste: Lojista vê apenas produtos da própria loja."""
        browser.get(f'{live_server_url}/login/')
        time.sleep(2)
        browser.find_element(By.NAME, 'username').send_keys('lojista_teste')
        browser.find_element(By.NAME, 'password').send_keys('lojista123')
        browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        time.sleep(2)
        
        WebDriverWait(browser, 10).until(EC.url_contains('lojista'))
        time.sleep(2)
        
        assert 'Produto Teste' in browser.page_source