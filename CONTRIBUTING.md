# Guia de Contribuição para o Projeto Smart Mall

Seja bem-vindo(a) ao Smart Mall. Este projeto é uma aplicação Django que simula um shopping virtual, com vitrines públicas, cadastro de lojas, gerenciamento de produtos, autenticação de lojistas e painel administrativo.

Este guia explica como preparar o ambiente local, executar testes, propor alterações e reportar problemas de forma organizada.

## Como Você Pode Contribuir

Você pode contribuir de diferentes formas:

- Implementando funcionalidades planejadas no backlog do Jira.
- Corrigindo bugs registrados nas Issues do GitHub.
- Melhorando telas, templates, estilos e fluxos existentes.
- Criando ou atualizando testes automatizados.
- Melhorando documentação, scripts e configuração de CI/CD.

Antes de começar, confira se já existe uma issue ou tarefa relacionada para evitar trabalho duplicado.

## Preparando o Ambiente

### 1. Faça um Fork do Repositório

Crie uma cópia do repositório principal na sua conta do GitHub:

🔗 [Fork do Smart Mall](https://github.com/eduardommb/smartmall-cesar/fork)

### 2. Clone o Seu Fork

Substitua `[SuaConta]` pelo seu usuário do GitHub:

```bash
git clone https://github.com/[SuaConta]/smartmall-cesar.git
cd smartmall-cesar
```

### 3. Crie uma Branch

Use nomes curtos e descritivos:

```bash
git checkout -b feature/nova-funcionalidade
git checkout -b fix/correcao-login
git checkout -b docs/atualiza-readme
```

## Configurando o Ambiente Local

### 1. Crie e Ative um Ambiente Virtual

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/Mac:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Instale as Dependências

```bash
pip install -r requirements.txt
```

### 3. Configure Variáveis de Ambiente

Para desenvolvimento local, o projeto possui valores padrão em `core/config/settings.py`. Em produção e CI/CD, use variáveis de ambiente.

Variáveis úteis:

```env
SECRET_KEY=sua-chave-secreta
DATABASE_URL=postgres://usuario:senha@host:porta/banco
ALLOWED_HOSTS=localhost,127.0.0.1
SERVE_MEDIA_FILES=true
```

Não envie arquivos `.env`, banco local (`db.sqlite3`) ou credenciais para o GitHub.

### 4. Aplique as Migrações

```bash
python manage.py migrate
```

### 5. Execute o Servidor

```bash
python manage.py runserver
```

A aplicação ficará disponível em:

```text
http://127.0.0.1:8000/
```

## Executando Testes

O projeto usa `pytest`, `pytest-django` e Selenium para testes E2E.

Para executar a suíte configurada:

```bash
pytest
```

Para rodar um arquivo específico:

```bash
pytest core/tests/test_auth.py
```

Para filtrar por nome:

```bash
pytest -k login
```

Os testes E2E usam Chrome/WebDriver. Em ambientes de CI, configure o navegador em modo headless quando necessário.

## Fluxo de Commits e Pull Requests

Siga mensagens curtas e objetivas, de preferência no padrão usado no histórico do projeto:

```text
FIX: Corrige login do lojista
UPDATE: Adiciona pipeline CI/CD
DOCS: Atualiza guia de contribuição
```

Antes de abrir uma Pull Request:

- Execute os testes relevantes.
- Descreva claramente o que foi alterado.
- Informe como a alteração foi testada.
- Vincule a issue ou tarefa do Jira, quando houver.
- Inclua prints ou vídeos em mudanças visuais.

## CI/CD e Deploy

O projeto utiliza GitHub Actions para validar alterações e acionar o deploy no Render. O deploy automático do Render deve permanecer desativado quando o fluxo oficial for via pipeline.

O workflow deve:

- Rodar em push ou pull request para `main`.
- Instalar dependências.
- Executar migrações.
- Executar `collectstatic`.
- Rodar os testes.
- Acionar o Deploy Hook do Render somente após sucesso dos testes.

Secrets necessários no GitHub Actions:

```text
SECRET_KEY
RENDER_DEPLOY_HOOK
```

## Como Reportar Bugs

Use a aba **Issues** do GitHub para registrar bugs, falhas e melhorias.

Ao abrir uma issue, inclua:

- Descrição objetiva do problema.
- Passos para reproduzir.
- Resultado esperado.
- Resultado obtido.
- Prints, logs ou vídeos, se possível.
- Navegador e ambiente usados.

Exemplo:

```text
Ao tentar editar um produto sem imagem, o formulário retorna erro.
Passos:
1. Entrar como lojista.
2. Abrir o dashboard.
3. Clicar em Editar Produto.
4. Salvar sem enviar nova imagem.
```

## Boas Práticas

- Não altere `manage.py` sem necessidade.
- Mantenha templates em `core/templates/`.
- Mantenha CSS e JavaScript em `core/static/core/`.
- Prefira nomes em português já usados no domínio, como `Loja`, `Produto`, `Categoria` e `lojista`.
- Não misture refatorações grandes com correções pequenas na mesma Pull Request.

## Referências

- [README do projeto](README.md)
- [Documentação do Django](https://docs.djangoproject.com/)
- [Documentação do pytest](https://docs.pytest.org/)
- [Documentação do Selenium](https://www.selenium.dev/documentation/)
- [GitHub Actions](https://docs.github.com/pt/actions)
- [Pull Requests no GitHub](https://docs.github.com/pt/pull-requests)
