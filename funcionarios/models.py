from django.db.models.functions import Upper
from django.db import models
from Clientes.models import Pessoa


class Funcionario(Pessoa):
    salario = models.DecimalField('Salário', max_digits=8, decimal_places=2, help_text='Salário base do funcionário')
    foto = models.ImageField('Foto', null=True, blank=True)
    cpf_cnpj = models.CharField('CPF', max_length=11, null=True, blank=True, unique=True,
                                help_text='Digite o CPF do Funcionário')
    nome = models.CharField('Nome', max_length=100, help_text='Nome completo')


    class Meta:
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'
        ordering = [Upper('nome')]
        permissions = (
            ('visualizar_funcionario', 'Pode visualizar a lista de funcionários'),
            ('cadastrar_funcionario', 'Pode cadastrar novos funcionários'),
            ('editar_funcionario', 'Pode editar funcionários existentes'),
            ('deletar_funcionario', 'Pode deletar funcionários'),
        )