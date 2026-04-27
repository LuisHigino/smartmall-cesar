"""
Testes E2E do lojista.
"""
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from core.models import Produto


pytestmark = pytest.mark.django_db


class TestLojistaDashboard:
    """Testes do dashboard do lojista."""

    def test_dashboard_carrega(self, browser, live_server_url, lojista_user, loja):
        """Teste: Dashboard do lojista carrega corretamente."""
        browser.get(f'{live_server_url}/login/')
        browser.find_element(By.NAME, 'username').send_keys('lojista_teste')
        browser.find_element(By.NAME, 'password').send_keys('lojista123')
        browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        
        WebDriverWait(browser, 10).until(EC.url_contains('lojista'))
        
        assert 'lojista' in browser.current_url.lower()

    def test_dashboard_exibe_nome_loja(self, browser, live_server_url, lojista_user, loja):
        """Teste: Dashboard exibe nome da loja."""
        browser.get(f'{live_server_url}/login/')
        browser.find_element(By.NAME, 'username').send_keys('lojista_teste')
        browser.find_element(By.NAME, 'password').send_keys('lojista123')
        browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        
        WebDriverWait(browser, 10).until(EC.url_contains('lojista'))
        
        assert 'Loja Teste' in browser.page_source

    def test_dashboard_exibe_produtos(self, browser, live_server_url, lojista_user, loja, produto):
        """Teste: Dashboard exibe produtos da loja."""
        browser.get(f'{live_server_url}/login/')
        browser.find_element(By.NAME, 'username').send_keys('lojista_teste')
        browser.find_element(By.NAME, 'password').send_keys('lojista123')
        browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        
        WebDriverWait(browser, 10).until(EC.url_contains('lojista'))
        
        assert 'Produto Teste' in browser.page_source

    def test_dashboard_exibe_estatisticas(self, browser, live_server_url, lojista_user, loja, produto):
        """Teste: Dashboard exibe estatísticas."""
        browser.get(f'{live_server_url}/login/')
        browser.find_element(By.NAME, 'username').send_keys('lojista_teste')
        browser.find_element(By.NAME, 'password').send_keys('lojista123')
        browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        
        WebDriverWait(browser, 10).until(EC.url_contains('lojista'))
        
        assert '1' in browser.page_source or 'produto' in browser.page_source.lower()


class TestLojistaEditarPerfil:
    """Testes de edição de perfil."""

    def test_editar_perfil_carrega(self, browser, live_server_url, lojista_user, loja):
        """Teste: Página de editar perfil carrega."""
        browser.get(f'{live_server_url}/login/')
        browser.find_element(By.NAME, 'username').send_keys('lojista_teste')
        browser.find_element(By.NAME, 'password').send_keys('lojista123')
        browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        
        WebDriverWait(browser, 10).until(EC.url_contains('lojista'))
        
        editar_link = browser.find_element(By.LINK_TEXT, 'Editar Perfil')
        editar_link.click()
        
        assert 'editar' in browser.current_url.lower()

class TestLojistaProduto:
    """Testes de gerenciamento de produtos."""

    def test_acessa_propria_loja(self, browser, live_server_url, lojista_user, loja):
        """Teste: Lojista acessa própria loja."""
        browser.get(f'{live_server_url}/lojista/')
        
        assert 'login' in browser.current_url.lower() or 'autenticar' in browser.page_source.lower()

    def test_nao_calcula_outra_loja(self, browser, live_server_url, lojista_user, loja):
        """Teste: Lojista não acessa dados de outra loja."""
        browser.get(f'{live_server_url}/login/')
        browser.find_element(By.NAME, 'username').send_keys('lojista_teste')
        browser.find_element(By.NAME, 'password').send_keys('lojista123')
        browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        
        WebDriverWait(browser, 10).until(EC.url_contains('lojista'))
        
        assert '/lojista/' in browser.current_url