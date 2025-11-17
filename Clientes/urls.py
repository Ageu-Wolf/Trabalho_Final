from django.urls import path
from .views import ClientesView, ClienteAddView, ClienteUpdateView, ClienteDeleteView

urlpatterns = [
    path('clientes', ClientesView.as_view(), name='clientes'),  # Eu sugiro usar path('lista/', ...) aqui

    # A URL completa agora será: /clientes/adicionar/
    path('cliente/adicionar/', ClienteAddView.as_view(), name='cliente_adicionar'),

    # A URL completa agora será: /clientes/<int:pk>/editar/
    path('<int:pk>/editar/', ClienteUpdateView.as_view(), name='cliente_editar'),

    path('<int:pk>/apagar/', ClienteDeleteView.as_view(), name='cliente_apagar'),
]
