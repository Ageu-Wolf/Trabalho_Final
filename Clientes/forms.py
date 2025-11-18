# Clientes/forms.py (ATUALIZADO)

from django import forms
from .models import Cliente
from django.core.exceptions import ValidationError


class ClienteModelForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'fone', 'email', 'tipo', 'cpf_cnpj', 'foto']

        error_messages = {
            # Mensagens de erro mantidas
            'nome': {'required': 'O nome do cliente é um campo obrigatório'},
            'fone': {'required': 'O número do telefone do cliente é um campo obrigatório'},
            'email': {
                'required': 'O e-mail do cliente é um campo obrigatório',
                'invalid': 'Formato inválido para o e-mail. Exemplo: fulano@dominio.com',
                'unique': 'E-mail já cadastrado'
            },
            'cpf_cnpj': {'required': 'O campo CPF/CNPJ é obrigatório'}
        }

        # --- 1. Adicionando Classes para Máscaras (NOVO) ---
        widgets = {
            'fone': forms.TextInput(attrs={'class': 'form-control mask-telefone', 'placeholder': '(00) 00000-0000'}),
            # O campo CPF/CNPJ usará uma máscara que será definida via JS no template,
            # baseada na seleção do campo 'tipo'. Por enquanto, adicionamos a classe.
            'cpf_cnpj': forms.TextInput(attrs={'class': 'form-control mask-cpf-cnpj'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        cpf_cnpj = cleaned_data.get('cpf_cnpj')

        # --- 2. Validação Simples (CRUA) ---

        # Se o campo não está preenchido, retorna o erro de obrigatoriedade
        if not cpf_cnpj:
            self.add_error('cpf_cnpj', 'O campo CPF/CNPJ é obrigatório.')
            return cleaned_data

        # Remove caracteres que não são dígitos (máscara)
        doc_limpo = ''.join(filter(str.isdigit, cpf_cnpj))

        if not doc_limpo.isdigit():
            self.add_error('cpf_cnpj', 'O documento deve conter apenas números.')
            return cleaned_data

        elif tipo == 'F':  # Pessoa Física (CPF)
            # Verifica se tem o tamanho correto (11 dígitos para CPF)
            if len(doc_limpo) != 11:
                self.add_error('cpf_cnpj', 'CPF inválido: Deve ter 11 dígitos. Digite apenas os números.')

        elif tipo == 'J':  # Pessoa Jurídica (CNPJ)
            # Verifica se tem o tamanho correto (14 dígitos para CNPJ)
            if len(doc_limpo) != 14:
                self.add_error('cpf_cnpj', 'CNPJ inválido: Deve ter 14 dígitos. Digite apenas os números.')

        return cleaned_data