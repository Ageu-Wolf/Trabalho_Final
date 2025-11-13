# inicio/urls.py

from django.urls import path
from .views import IndexView # Certifique-se que IndexView existe e está correta

urlpatterns = [
    # A rota interna pode ser vazia, pois o caminho raiz ('') já foi definido no arquivo principal
    path('', IndexView.as_view(), name='index'),
]