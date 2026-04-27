"""
Testes E2E da vitrine pública.
"""
import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from core.models import Categoria, Loja, Produto


pytestmark = pytest.mark.django_db


class TestVitrine:
    """Testes da vitrine pública."""

    def test_vitrine_carrega(self, browser, live_server_url):
        """Teste: Vitrine carrega corretamente."""
        browser.get(f'{live_server_url}/vitrine/')
        time.sleep(2)
        
        assert 'SmartMall' in browser.page_source

    def test_vitrine_exibe_categorias(self, browser, live_server_url, categoria, categoria_lojas):
        """Teste: Vitrine exibe categorias."""
        browser.get(f'{live_server_url}/vitrine/')
        time.sleep(2)
        
        assert 'Restaurantes' in browser.page_source
        assert 'Lojas' in browser.page_source

    def test_vitrine_exibe_lojas(self, browser, live_server_url, loja):
        """Teste: Vitrine exibe lojas cadastradas."""
        browser.get(f'{live_server_url}/vitrine/')
        time.sleep(2)
        
        assert 'Loja Teste' in browser.page_source

    def test_filtro_categoria(self, browser, live_server_url, categoria, categoria_informatica, loja):
        """Teste: Filtro por categoria funciona."""
        browser.get(f'{live_server_url}/vitrine/')
        time.sleep(2)
        
        filtro_link = browser.find_element(By.CSS_SELECTOR, f'a[href*="categoria={categoria.id}"]')
        filtro_link.click()
        time.sleep(2)
        
        assert f'categoria={categoria.id}' in browser.current_url

    def test_redirect_home_para_vitrine(self, browser, live_server_url):
        """Teste: Acessar / redireciona para /vitrine/."""
        browser.get(f'{live_server_url}/')
        time.sleep(2)
        
        assert '/vitrine/' in browser.current_url


class TestNavbar:
    """Testes da navbar."""

    def test_navbar_nao_autenticado(self, browser, live_server_url):
        """Teste: Navbar mostra Login/Cadastre-se para não autenticado."""
        browser.get(f'{live_server_url}/vitrine/')
        time.sleep(2)
        
        assert 'Login' in browser.page_source or 'login' in browser.page_source.lower()

    def test_navbar_autenticado_admin(self, browser, live_server_url, admin_user):
        """Teste: Navbar mostra Meu Painel para admin."""
        browser.get(f'{live_server_url}/login/')
        time.sleep(2)
        browser.find_element(By.NAME, 'username').send_keys('admin')
        browser.find_element(By.NAME, 'password').send_keys('admin123')
        browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        time.sleep(2)
        
        WebDriverWait(browser, 10).until(EC.url_contains('admin'))
        time.sleep(2)
        
        assert 'admin' in browser.page_source.lower() or 'Painel' in browser.page_source

    def test_navbar_autenticado_lojista(self, browser, live_server_url, lojista_user, loja):
        """Teste: Navbar mostra Minha Loja para lojista."""
        browser.get(f'{live_server_url}/login/')
        time.sleep(2)
        browser.find_element(By.NAME, 'username').send_keys('lojista_teste')
        browser.find_element(By.NAME, 'password').send_keys('lojista123')
        browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        time.sleep(2)
        
        WebDriverWait(browser, 10).until(EC.url_contains('lojista'))
        time.sleep(2)
        
        assert 'lojista' in browser.current_url.lower()


class TestDetalheLoja:
    """Testes de detalhe de loja."""

    def test_acessa_detalhe_loja(self, browser, live_server_url, loja, produto):
        """Teste: Página de detalhe da loja carrega."""
        browser.get(f'{live_server_url}/loja/{loja.id}/')
        time.sleep(2)
        
        assert 'Loja Teste' in browser.page_source

    def test_detalhe_loja_exibe_produtos(self, browser, live_server_url, loja, produto):
        """Teste: Detalhe da loja exibe produtos."""
        browser.get(f'{live_server_url}/loja/{loja.id}/')
        time.sleep(2)
        
        assert 'Produto Teste' in browser.page_source