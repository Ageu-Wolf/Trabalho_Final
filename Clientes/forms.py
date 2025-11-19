# Clientes/forms.py (ATUALIZADO)

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
            'cpf_cnpj': {'required': 'O campo CPF/CNPJ é obrigatório'}
        }

        widgets = {
            'fone': forms.TextInput(attrs={'class': 'form-control mask-telefone', 'placeholder': '(00) 00000-0000'}),
            'cpf_cnpj': forms.TextInput(attrs={'class': 'form-control mask-cpf-cnpj'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        cpf_cnpj = cleaned_data.get('cpf_cnpj')


        if not cpf_cnpj:
            self.add_error('cpf_cnpj', 'O campo CPF/CNPJ é obrigatório.')
            return cleaned_data

        doc_limpo = ''.join(filter(str.isdigit, cpf_cnpj))

        if not doc_limpo.isdigit():
            self.add_error('cpf_cnpj', 'O documento deve conter apenas números.')
            return cleaned_data

        elif tipo == 'F':
            if len(doc_limpo) != 11:
                self.add_error('cpf_cnpj', 'CPF inválido: Deve ter 11 dígitos. Digite apenas os números.')

        elif tipo == 'J':
            if len(doc_limpo) != 14:
                self.add_error('cpf_cnpj', 'CNPJ inválido: Deve ter 14 dígitos. Digite apenas os números.')

        return cleaned_data