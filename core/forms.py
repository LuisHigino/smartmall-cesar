from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Produto, Loja, Categoria


class LojistaRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        label='E-mail',
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'seu@email.com'})
    )
    nome_loja = forms.CharField(
        label='Nome da Loja',
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Nome da sua loja'})
    )
    cnpj = forms.CharField(
        label='CNPJ',
        max_length=18,
        widget=forms.TextInput(attrs={'placeholder': 'XX.XXX.XXX/XXXX-XX'})
    )
    responsavel = forms.CharField(
        label='Nome do Responsável',
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Nome completo'})
    )
    categoria = forms.ModelChoiceField(
        label='Categoria',
        queryset=Categoria.objects.all(),
        required=True,
        empty_label='Selecione uma categoria'
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Usuário para login'}),
        }

    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj')
        if Loja.objects.filter(cnpj=cnpj).exists():
            raise forms.ValidationError('Este CNPJ já está cadastrado.')
        return cnpj

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este e-mail já está em uso.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_active = True
        if commit:
            user.save()

        loja = Loja.objects.create(
            nome=self.cleaned_data['nome_loja'],
            cnpj=self.cleaned_data['cnpj'],
            responsavel=self.cleaned_data['responsavel'],
            categoria=self.cleaned_data['categoria'],
            usuario=user
        )
        return user


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'preco', 'estoque', 'descricao', 'imagem', 'loja']


class LojaForm(forms.ModelForm):
    class Meta:
        model = Loja
        fields = ['nome', 'cnpj', 'responsavel', 'categoria']

    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj')
        existing = Loja.objects.filter(cnpj=cnpj)
        if self.instance and self.instance.pk:
            existing = existing.exclude(pk=self.instance.pk)
        if existing.exists():
            raise forms.ValidationError('CNPJ já cadastrado')
        return cnpj

