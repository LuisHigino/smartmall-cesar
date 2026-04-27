"""
Testes E2E de autenticação.
"""
import time
import pytest
from django.contrib.auth.models import User
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from core.models import Categoria, Loja


pytestmark = pytest.mark.django_db


class TestLogin:
    """Testes de login."""

    def test_pagina_login_carrega(self, browser, live_server_url):
        """Teste: Página de login carrega corretamente."""
        browser.get(f'{live_server_url}/login/')
        time.sleep(2)
        
        assert 'Login' in browser.page_source or 'Entrar' in browser.page_source
        assert 'login' in browser.current_url.lower()

    def test_login_admin_sucesso(self, browser, live_server_url, admin_user):
        """Teste: Login com usuário admin redireciona para admin-dashboard."""
        browser.get(f'{live_server_url}/login/')
        time.sleep(2)
        
        username_input = browser.find_element(By.NAME, 'username')
        password_input = browser.find_element(By.NAME, 'password')
        
        username_input.send_keys('admin')
        password_input.send_keys('admin123')
        password_input.send_keys(Keys.RETURN)
        time.sleep(2)
        
        WebDriverWait(browser, 10).until(
            EC.url_contains('admin-dashboard')
        )
        time.sleep(2)
        
        assert 'admin-dashboard' in browser.current_url

    def test_login_lojista_sucesso(self, browser, live_server_url, lojista_user, loja):
        """Teste: Login com lojista redireciona para dashboard do lojista."""
        browser.get(f'{live_server_url}/login/')
        time.sleep(2)
        
        username_input = browser.find_element(By.NAME, 'username')
        password_input = browser.find_element(By.NAME, 'password')
        
        username_input.send_keys('lojista_teste')
        password_input.send_keys('lojista123')
        password_input.send_keys(Keys.RETURN)
        time.sleep(2)
        
        WebDriverWait(browser, 10).until(
            EC.url_contains('lojista')
        )
        time.sleep(2)
        
        assert 'lojista' in browser.current_url

    def test_login_invalido(self, browser, live_server_url):
        """Teste: Login com credenciais inválidas mostra erro."""
        browser.get(f'{live_server_url}/login/')
        time.sleep(2)
        
        username_input = browser.find_element(By.NAME, 'username')
        password_input = browser.find_element(By.NAME, 'password')
        
        username_input.send_keys('usuario_invalido')
        password_input.send_keys('senha_errada')
        password_input.send_keys(Keys.RETURN)
        time.sleep(2)
        
        WebDriverWait(browser, 5).until(
            EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), 'incorreto')
        )
        time.sleep(2)
        
        assert 'login' in browser.current_url.lower()


class TestLogout:
    """Testes de logout."""

    def test_logout_botao_existe(self, browser, live_server_url, admin_user):
        """Teste: Botão de logout existe após login."""
        browser.get(f'{live_server_url}/login/')
        time.sleep(2)
        
        username_input = browser.find_element(By.NAME, 'username')
        password_input = browser.find_element(By.NAME, 'password')
        
        username_input.send_keys('admin')
        password_input.send_keys('admin123')
        password_input.send_keys(Keys.RETURN)
        time.sleep(2)
        
        WebDriverWait(browser, 10).until(
            EC.url_contains('admin-dashboard')
        )
        time.sleep(2)
        
        logout_link = browser.find_element(By.LINK_TEXT, 'Sair')
        assert logout_link is not None


class TestRegistroLojista:
    """Testes de registro de lojista."""

    def test_pagina_registro_carrega(self, browser, live_server_url):
        """Teste: Página de registro carrega corretamente."""
        browser.get(f'{live_server_url}/registro-lojista/')
        time.sleep(2)
        
        assert 'Cadastrar' in browser.page_source
        assert 'registro' in browser.current_url.lower()

    def test_registro_cnpj_duplicado(self, browser, live_server_url, loja, categoria):
        """Teste: Registro com CNPJ duplicado mostra erro."""
        browser.get(f'{live_server_url}/registro-lojista/')
        time.sleep(2)
        
        browser.find_element(By.NAME, 'username').send_keys('outro_lojista')
        browser.find_element(By.NAME, 'email').send_keys('outro@teste.com')
        browser.find_element(By.NAME, 'password1').send_keys('Senha@123')
        browser.find_element(By.NAME, 'password2').send_keys('Senha@123')
        browser.find_element(By.NAME, 'nome_loja').send_keys('Outra Loja')
        
        browser.find_element(By.NAME, 'cnpj').send_keys(loja.cnpj)
        browser.find_element(By.NAME, 'responsavel').send_keys('João')
        browser.find_element(By.NAME, 'categoria').send_keys(str(categoria.id))
        
        browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        time.sleep(2)
        
        assert 'CNPJ' in browser.page_source or 'já cadastrado' in browser.page_source.lower()


class TestRedirecionamento:
    """Testes de redirecionamento pós-login."""

    def test_admin_vai_para_admin_dashboard(self, browser, live_server_url, admin_user):
        """Teste: Admin é redirecionado para admin-dashboard após login."""
        browser.get(f'{live_server_url}/login/')
        time.sleep(2)
        
        browser.find_element(By.NAME, 'username').send_keys('admin')
        browser.find_element(By.NAME, 'password').send_keys('admin123')
        browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        time.sleep(2)
        
        WebDriverWait(browser, 10).until(
            EC.url_contains('admin-dashboard')
        )
        time.sleep(2)
        
        assert 'admin-dashboard' in browser.current_url

    def test_lojista_vai_para_dashboard(self, browser, live_server_url, lojista_user, loja):
        """Teste: Lojista é redirecionado para dashboard após login."""
        browser.get(f'{live_server_url}/login/')
        time.sleep(2)
        
        browser.find_element(By.NAME, 'username').send_keys('lojista_teste')
        browser.find_element(By.NAME, 'password').send_keys('lojista123')
        browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        time.sleep(2)
        
        WebDriverWait(browser, 10).until(
            EC.url_contains('lojista')
        )
        time.sleep(2)
        
        assert '/lojista/' in browser.current_url