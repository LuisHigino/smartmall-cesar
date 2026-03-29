from django.urls import path
from .views import shopping_view

urlpatterns = [
    path('', shopping_view),
]