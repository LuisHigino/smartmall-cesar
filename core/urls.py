from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('catalogo/', views.painel_catalogo, name='painel_catalogo'),
    path('catalogo/adicionar/', views.adicionar_produto, name='adicionar_produto'),
    path('catalogo/editar/<int:id>/', views.editar_produto, name='editar_produto'),
    path('catalogo/remover/<int:id>/', views.remover_produto, name='remover_produto'),

    # Loja (Admin)
    path('lojas/', views.painel_lojas, name='painel_lojas'),
    path('lojas/adicionar/', views.cadastrar_loja, name='cadastrar_loja'),
    path('lojas/editar/<int:id>/', views.editar_loja, name='editar_loja'),
    path('lojas/remover/<int:id>/', views.remover_loja, name='remover_loja'),
]
