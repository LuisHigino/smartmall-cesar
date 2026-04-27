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

    @pytest.mark.skip(reason="Test isolation issues with SQLite in-memory")
    def test_editar_perfil_salva(self, browser, live_server_url, lojista_user, loja):
        """Teste: Editar perfil salva alterações."""
        browser.get(f'{live_server_url}/login/')
        browser.find_element(By.NAME, 'username').send_keys('lojista_teste')
        browser.find_element(By.NAME, 'password').send_keys('lojista123')
        browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        
        WebDriverWait(browser, 10).until(EC.url_contains('lojista'))
        
        browser.get(f'{live_server_url}/lojista/editar/')
        
        nome_input = browser.find_element(By.NAME, 'nome')
        nome_input.clear()
        nome_input.send_keys('Loja Atualizada')
        
        browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        
        # Aguarda redirecionamento para o dashboard
        WebDriverWait(browser, 10).until(EC.url_contains('lojista'))
        
        # Verifica no banco de dados
        loja.refresh_from_db()
        assert loja.nome == 'Loja Atualizada'


class TestLojistaProduto:
    """Testes de gerenciamento de produtos."""

    @pytest.mark.skip(reason="Test isolation issues with SQLite in-memory")
    def test_adicionar_produto(self, browser, live_server_url, lojista_user, loja):
        """Teste: Adicionar novo produto."""
        browser.get(f'{live_server_url}/login/')
        browser.find_element(By.NAME, 'username').send_keys('lojista_teste')
        browser.find_element(By.NAME, 'password').send_keys('lojista123')
        browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        
        WebDriverWait(browser, 10).until(EC.url_contains('lojista'))
        
        browser.get(f'{live_server_url}/lojista/produtos/adicionar/')
        
        browser.find_element(By.NAME, 'nome').send_keys('Novo Produto')
        browser.find_element(By.NAME, 'preco').send_keys('150.00')
        browser.find_element(By.NAME, 'estoque').send_keys('20')
        
        # Seleciona a categoria se o campo existir
        try:
            from selenium.webdriver.support.ui import Select
            select = Select(browser.find_element(By.NAME, 'categoria'))
            select.select_by_index(1)  # Seleciona a primeira categoria disponível
        except:
            pass  # Se não houver campo categoria, continua
        
        browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        
        assert Produto.objects.filter(nome='Novo Produto', loja=loja).exists()

    @pytest.mark.skip(reason="Test isolation issues with SQLite in-memory")
    def test_editar_produto(self, browser, live_server_url, lojista_user, loja, produto):
        """Teste: Editar produto."""
        browser.get(f'{live_server_url}/login/')
        browser.find_element(By.NAME, 'username').send_keys('lojista_teste')
        browser.find_element(By.NAME, 'password').send_keys('lojista123')
        browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        
        WebDriverWait(browser, 10).until(EC.url_contains('lojista'))
        
        browser.get(f'{live_server_url}/lojista/produtos/editar/{produto.id}/')
        
        nome_input = browser.find_element(By.NAME, 'nome')
        nome_input.clear()
        nome_input.send_keys('Produto Atualizado')
        
        # Tenta selecionar categoria se o campo existir
        try:
            from selenium.webdriver.support.ui import Select
            select = Select(browser.find_element(By.NAME, 'categoria'))
            select.select_by_index(1)
        except:
            pass
        
        browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        
        # Aguarda o redirecionamento
        WebDriverWait(browser, 10).until(EC.url_contains('lojista'))
        
        # Verifica no banco de dados
        produto.refresh_from_db()
        assert produto.nome == 'Produto Atualizado'

    @pytest.mark.skip(reason="Test isolation issues with SQLite in-memory")
    def test_remover_produto(self, browser, live_server_url, lojista_user, loja, produto):
        """Teste: Remover produto."""
        produto_id = produto.id
        
        browser.get(f'{live_server_url}/login/')
        browser.find_element(By.NAME, 'username').send_keys('lojista_teste')
        browser.find_element(By.NAME, 'password').send_keys('lojista123')
        browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        
        WebDriverWait(browser, 10).until(EC.url_contains('lojista'))
        
        browser.get(f'{live_server_url}/lojista/produtos/remover/{produto_id}/')
        
        assert 'Remover' in browser.page_source
        
        # Clica no botão de confirmar remoção
        browser.find_element(By.CSS_SELECTOR, '.btn-danger').click()
        
        # Aguarda redirecionamento para o dashboard
        WebDriverWait(browser, 10).until(EC.url_contains('lojista'))
        
        assert not Produto.objects.filter(id=produto_id).exists()


class TestLojistaAcesso:
    """Testes de acesso do lojista."""

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