from django.urls import path
from . import views

urlpatterns = [
    path('catalogo/', views.painel_catalogo, name='painel_catalogo'),
    path('catalogo/adicionar/', views.adicionar_produto, name='adicionar_produto'),
    path('catalogo/editar/<int:id>/', views.editar_produto, name='editar_produto'),
    path('catalogo/remover/<int:id>/', views.remover_produto, name='remover_produto'),
]
