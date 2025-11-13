from django.urls import path
from .views import VagasView, EstacionamentoCreateView, CalculoPagamentoView, ConfirmacaoPagamentoView

urlpatterns = [

    path('', VagasView.as_view(), name='Vagas'),

    path('entrada/', EstacionamentoCreateView.as_view(), name='estacionamento_entrada'),

    path('saida/<int:pk>/', CalculoPagamentoView.as_view(), name='calculo_pagamento'),

    path('pagar/<int:pk>/', ConfirmacaoPagamentoView.as_view(), name='confirmacao_pagamento'),]