from django import forms
from .models import Carro

class CarroForm(forms.ModelForm):
    class Meta:
        model = Carro
        fields = ['placa', 'modelo', 'cor', 'clientes']

        error_messages = {
            'placa': {
                'required': 'A placa do carro é obrigatória',
                'unique': 'Esta placa já está cadastrada',
            },
            'modelo': {
                'required': 'O modelo do carro é obrigatório',
            },
            'cor': {
                'required': 'A cor do carro é obrigatória',
            },
            'clientes': {
                'required': 'Quem são os donos?',
            },
        }