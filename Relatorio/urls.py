from django.urls import path
from .views import RelatorioListView

urlpatterns = [
    # Caminho principal para listar os relatórios
    path('', RelatorioListView.as_view(), name='relatorios_lista'),
]