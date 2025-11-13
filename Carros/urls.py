from django.urls import path
from .views import CarrosView, CarroAddView, CarroUpdateView, CarroDeleteView,CarroDetailView

urlpatterns = [
    path('Carros/', CarrosView.as_view(), name='carros'),

    path('carro/adicionar/', CarroAddView.as_view(), name='carro_adicionar'),

    path('carro/<str:pk>/editar/', CarroUpdateView.as_view(), name='carro_editar'),

    path('<str:pk>/apagar/', CarroDeleteView.as_view(), name='carro_apagar'),

    path('carro/<str:pk>/', CarroDetailView.as_view(), name='carro_detalhe'),
]
