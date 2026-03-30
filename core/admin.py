from django.contrib import admin
from .models import Produto, Loja, Categoria

admin.site.register(Produto)
admin.site.register(Loja)
admin.site.register(Categoria)