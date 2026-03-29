from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Loja


class LojaAdminTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username='admin', email='admin@example.com', password='adminpwd')
        self.client.login(username='admin', password='adminpwd')

    def test_cadastro_loja_com_sucesso(self):
        response = self.client.post(
            reverse('cadastrar_loja'),
            {
                'nome': 'Loja Teste',
                'cnpj': '12.345.678/0001-99',
                'responsavel': 'Carlos Silva',
            },
            follow=True,
        )
        self.assertContains(response, 'Loja cadastrada com sucesso')

        loja = Loja.objects.get(cnpj='12.345.678/0001-99')
        self.assertEqual(loja.nome, 'Loja Teste')
        self.assertEqual(loja.responsavel, 'Carlos Silva')
        self.assertIsNotNone(loja.usuario)
        self.assertEqual(loja.usuario.username, '12345678000199')

    def test_cadastro_loja_cnpj_ja_cadastrado(self):
        Loja.objects.create(nome='Loja Existente', cnpj='12.345.678/0001-99', responsavel='Servidor')

        response = self.client.post(
            reverse('cadastrar_loja'),
            {
                'nome': 'Outra Loja',
                'cnpj': '12.345.678/0001-99',
                'responsavel': 'José',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertTrue(form.errors)
        self.assertIn('cnpj', form.errors)
        self.assertEqual(form.errors['cnpj'][0], 'CNPJ já cadastrado')
        self.assertEqual(Loja.objects.filter(cnpj='12.345.678/0001-99').count(), 1)

    def test_editar_loja_com_sucesso(self):
        loja = Loja.objects.create(nome='Loja Original', cnpj='12.345.678/0001-99', responsavel='Original')

        response = self.client.post(
            reverse('editar_loja', args=[loja.id]),
            {
                'nome': 'Loja Editada',
                'cnpj': '12.345.678/0001-99',
                'responsavel': 'Editado',
            },
            follow=True,
        )
        self.assertContains(response, 'Loja atualizada com sucesso')

        loja.refresh_from_db()
        self.assertEqual(loja.nome, 'Loja Editada')
        self.assertEqual(loja.responsavel, 'Editado')

    def test_remover_loja_com_sucesso(self):
        loja = Loja.objects.create(nome='Loja Para Remover', cnpj='12.345.678/0001-99', responsavel='Remover')

        response = self.client.post(
            reverse('remover_loja', args=[loja.id]),
            follow=True,
        )
        self.assertContains(response, 'Loja removida com sucesso')

        self.assertFalse(Loja.objects.filter(id=loja.id).exists())

