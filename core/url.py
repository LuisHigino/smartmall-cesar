from django.urls import path
from . import views
urlpatterns = [
    path('adicionar/', views.adicionar_produto, name='adicionar_produto'),
]