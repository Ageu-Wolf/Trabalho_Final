
from django.db import models
from django.db.models.functions import Upper

TIPO_PESSOA_CHOICES = [
    ('F', 'Pessoa Física'),
    ('J', 'Pessoa Jurídica'),
]


class Pessoa(models.Model):
    nome = models.CharField('Nome', max_length=100, help_text='Nome completo ou razão social')
    tipo = models.CharField('Tipo de Pessoa', max_length=1, choices=TIPO_PESSOA_CHOICES, default='F')
    cpf_cnpj = models.CharField('CPF/CNPJ', max_length=18, null=True, blank=True, unique=True,
                                help_text='CPF para Pessoa Física, CNPJ para Pessoa Jurídica')
    foto = models.ImageField('Foto', null=True, blank=True)

    class Meta:
        abstract = True
        ordering = [Upper('nome')]
        permissions = (
            ('visualizar_cliente', 'Pode visualizar a lista e detalhes de clientes'),
            ('cadastrar_cliente', 'Pode adicionar novos clientes'),
            ('editar_cliente', 'Pode editar clientes existentes'),
            ('deletar_cliente', 'Pode excluir clientes'))

    def __str__(self):
        return self.nome


class Cliente(Pessoa):
    fone = models.CharField('Telefone', max_length=15, help_text='Número do telefone')
    email = models.CharField('Email', max_length=100, help_text='Endereço de Email', unique=True)
    carros = models.ManyToManyField('Carros.Carro', blank=True, verbose_name='Carros do Cliente')
