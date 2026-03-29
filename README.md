# **Smart Mall**

Propomos a ideia de um **Smart Mall**, Shopping inteligente(e-commerce); onde a ideia parte da perspectiva de você ter um shopping na palma de sua mão(mobile ou desktop) e possa usufruir dos serviços dele sem sair de casa.Uma Loja virtual, mas num ecossistema de um shopping.

A ideia de shopping se dá uma vez que nos abre um leque bem vasto de possíveis histórias de usuário e ao mesmo tempo que pode ser limitado pelo “tamanho” do shopping ou pela quantidade lojas. Tornando-o uma espécie de galeria, um shopping na palma de sua mão.

## **Membros da equipe**

1. **LUCAS BERENGUER AVELINO DE SOUZA**
2. **LUIZ EDUARDO MARTINS BRAGA**
3. **LUIS FELIPE HIGINO MOURA**
4. **MATHEUS GUERRA BRITTO**
5. **ELIAN GABRIEL ANDRADE CUNHA**
6. **BRENO DE GODOY SANTIAGO**


## 📦 **Entregas**

<details>
<summary><strong>🎯 Entrega 01</strong></summary>

### Histórias de Usuário
🔗 [ Link para o PDF das histórias](https://drive.google.com/file/d/1Iw43bgSYVKJMoOHrVAX-ubfhxd2VfMrN/view?usp=sharing)

### Quadro da Entrega
[📄 Link para o Quadro](https://matheus-guerra-britto.atlassian.net/jira/software/projects/PF/boards/34?atlOrigin=eyJpIjoiOTRlNDBlZTI3Nzc5NGZhZGEyMDE1NGY5YmVmYjY5ZTkiLCJwIjoiaiJ9)

### Figma
[📲 Link para o protótipo Lo-Fi](https://www.figma.com/board/vSDqHps0Z33oV9mkjktN6I/Projeto---Smart-Mall?node-id=0-1&p=f&t=eDLrNBHWh9KLbcQ5-0)

### Vídeo do Protótipo Lo-Fi
[🔗 Link para o vídeo](https://youtu.be/fkxZygw4R_Q)

</details>

<details>
<summary><strong>🎯 Entrega 02</strong></summary>

<details>
<summary><strong>Cadastro de Lojista</strong></summary>

# Implementação da História: Cadastro de Lojista

## Descrição da História

**Como administrador do shopping, eu quero cadastrar uma nova loja na plataforma, para que ela possa começar a vender seus itens.**

**Ação no BD: ESCRITA (Cria um registro na tabela Loja e Usuario).**

## Cenários de Avaliação (BDD)

### Cenário 1: Cadastro de nova loja com sucesso
- **Dado** que estou logado no sistema com perfil de Administrador
- **Quando** eu preencho os dados obrigatórios da nova loja (nome, CNPJ, responsável) e clico em "Salvar"
- **Então** o sistema exibe uma mensagem de sucesso ("Loja cadastrada com sucesso") e os registros são criados nas tabelas de Loja e Usuario.

### Cenário 2: Tentativa de cadastro com CNPJ já existente
- **Dado** que estou na tela de cadastro de lojas
- **Quando** eu insiro um CNPJ que já está registrado na base de dados
- **Então** o sistema deve exibir uma mensagem de erro ("CNPJ já cadastrado") e bloquear a criação do registro.

## Implementação Técnica

### Modelo de Dados

#### Loja
- `nome`: CharField (max_length=255) - Nome da loja
- `cnpj`: CharField (max_length=18, unique=True) - CNPJ da loja
- `responsavel`: CharField (max_length=255) - Nome do responsável
- `usuario`: OneToOneField(User, on_delete=PROTECT, null=True, blank=True) - Usuário associado
- `criado_em`: DateTimeField (auto_now_add=True) - Data de criação

#### Usuario (Django Auth)
- Criado automaticamente com:
  - `username`: CNPJ sem pontuação (ex: "12345678000199")
  - `password`: Senha aleatória gerada
  - `first_name`: Nome do responsável
  - `is_active`: True

### Validações
- CNPJ único na tabela Loja
- Campos obrigatórios: nome, cnpj, responsavel

### Views Implementadas
- `home`: Página inicial com links para catálogo e gestão de lojas
- `painel_lojas`: Lista todas as lojas cadastradas
- `cadastrar_loja`: Formulário para criar nova loja
- `editar_loja`: Formulário para editar loja existente
- `remover_loja`: Confirmação e remoção de loja

### URLs
- `/`: Home
- `/lojas/`: Painel de lojas
- `/lojas/adicionar/`: Cadastrar loja
- `/lojas/editar/<id>/`: Editar loja
- `/lojas/remover/<id>/`: Remover loja

### Templates
- `home.html`: Página inicial
- `lojas.html`: Lista de lojas com ações
- `cadastrar_loja.html`: Formulário de cadastro/edição
- `remover_loja.html`: Confirmação de remoção

### Segurança
- Todas as views de loja requerem login (`@login_required`)
- Apenas usuários staff (`@user_passes_test(lambda u: u.is_staff)`) podem acessar

### Testes Unitários
- `test_cadastro_loja_com_sucesso`: Verifica criação de loja e usuário
- `test_cadastro_loja_cnpj_ja_cadastrado`: Verifica bloqueio de CNPJ duplicado
- `test_editar_loja_com_sucesso`: Verifica edição de loja
- `test_remover_loja_com_sucesso`: Verifica remoção de loja

## Como Usar

1. Acesse `/admin/` e crie um superusuário
2. Logue como admin
3. Vá para `/lojas/adicionar/`
4. Preencha nome, CNPJ e responsável
5. Clique em "Salvar"
6. A loja será criada e um usuário será gerado automaticamente

## Dependências
- Django==6.0.3
- Pillow==12.1.1
- asgiref==3.11.1
- sqlparse==0.5.5
- tzdata==2025.3

## Arquivos Modificados/Criados
- `core/models.py`: Adicionado modelo Loja
- `core/forms.py`: Adicionado LojaForm
- `core/views.py`: Adicionadas views de loja
- `core/urls.py`: Adicionadas URLs de loja
- `core/admin.py`: Registrado Loja no admin
- `core/tests.py`: Adicionados testes BDD
- `core/templates/`: Criados templates para loja
- `requirements.txt`: Gerado com dependências
- `core/migrations/`: Migração para Loja

## Status
✅ Implementado e testado
✅ Mergeado para main
✅ Pronto para o uso dos manos

### Documentação
🔗 [ Link para documentação](https://docs.google.com/document/d/1jGei-4t01ZkQrpn4vyDz3BRtzGOarXBmsQENuux9Kw0/edit?tab=t.0)


### Vídeo da Implementação
[🔗 Link para o vídeo](https://www.youtube.com/watch?v=eiBkOGZw2K8)

### Quadro da Entrega
[📄 Link para o Quadro](https://matheus-guerra-britto.atlassian.net/jira/software/projects/PF/boards/34?atlOrigin=eyJpIjoiOTRlNDBlZTI3Nzc5NGZhZGEyMDE1NGY5YmVmYjY5ZTkiLCJwIjoiaiJ9)


</details>

</details>