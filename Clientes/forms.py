# Clientes/forms.py (Ajustado)

from django import forms
from .models import Cliente


class ClienteModelForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'fone', 'email', 'tipo', 'cpf_cnpj', 'foto']

        error_messages = {
            'nome': {'required': 'O nome do cliente é um campo obrigatório'},
            'fone': {'required': 'O número do telefone do cliente é um campo obrigatório'},
            'email': {
                'required': 'O e-mail do cliente é um campo obrigatório',
                'invalid': 'Formato inválido para o e-mail. Exemplo: fulano@dominio.com',
                'unique': 'E-mail já cadastrado'
            },
            'cpf_cnpj': {'required': 'CPF/CNPJ é um campo obrigatório para qualquer Pessoa'}
        }

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        cpf_cnpj = cleaned_data.get('cpf_cnpj')

        if not cpf_cnpj:
            self.add_error('cpf_cnpj', 'O campo CPF/CNPJ é obrigatório.')

        return cleaned_data