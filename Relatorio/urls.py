from django.urls import path
from .views import RelatorioListView

urlpatterns = [
    path('', RelatorioListView.as_view(), name='relatorios_lista'),
]