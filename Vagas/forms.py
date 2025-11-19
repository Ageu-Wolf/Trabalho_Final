from django import forms
from .models import Estacionamento

class EstacionamentoEntradaForm(forms.ModelForm):

    class Meta:
        model = Estacionamento
        fields = ['carro', 'funcionario', 'cliente', 'periodo_estimado', 'relatorio']

        widgets = {
            'relatorio': forms.Textarea(attrs={'rows': 3, 'class': 'form-control rounded-pill'})}

class PagamentoForm(forms.Form):
    METODOS_PAGAMENTO = [
        ('DINHEIRO', 'Dinheiro'),
        ('DEBITO', 'Débito'),
        ('CREDITO', 'Crédito (+5% de taxa)'),
        ('PIX', 'Pix (-5% de desconto)'),
    ]

    metodo_pagamento = forms.ChoiceField(
        choices=METODOS_PAGAMENTO,
        widget=forms.RadioSelect,
        label="Escolha o Método de Pagamento"
    )