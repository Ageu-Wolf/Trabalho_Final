
from django.urls import path
from .views import (
    FuncionarioListView,
    FuncionarioCreateView,
    FuncionarioUpdateView,
    FuncionarioDeleteView
)

urlpatterns = [
    path('', FuncionarioListView.as_view(), name='funcionarios'),
    path('adicionar/', FuncionarioCreateView.as_view(), name='funcionario_adicionar'),
    path('editar/<int:pk>/', FuncionarioUpdateView.as_view(), name='funcionario_editar'),
    path('apagar/<int:pk>/', FuncionarioDeleteView.as_view(), name='funcionario_apagar'),
]