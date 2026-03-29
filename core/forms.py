from django import forms
from .models import Produto, Loja

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'preco', 'estoque', 'descricao', 'imagem']


class LojaForm(forms.ModelForm):
    class Meta:
        model = Loja
        fields = ['nome', 'cnpj', 'responsavel']

    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj')
        existing = Loja.objects.filter(cnpj=cnpj)
        if self.instance and self.instance.pk:
            existing = existing.exclude(pk=self.instance.pk)
        if existing.exists():
            raise forms.ValidationError('CNPJ já cadastrado')
        return cnpj

