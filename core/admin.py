from django.contrib import admin
from .models import Loja, Produto, Categoria

@admin.register(Loja)
class LojaAdmin(admin.ModelAdmin):
    list_display = ("nome", "cnpj", "responsavel", "categoria", "criado_em", "usuario")
    search_fields = ("nome", "cnpj", "responsavel", "usuario__username")
    list_filter = ("categoria", "criado_em")
    ordering = ("nome",)

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("nome", "preco", "estoque")
    search_fields = ("nome",)
    list_filter = ()
    ordering = ("nome",)

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome",)
    search_fields = ("nome",)
    ordering = ("nome",)