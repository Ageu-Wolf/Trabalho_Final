from django.db.models.functions import Upper
from django.db import models
from Clientes.models import Pessoa


class Funcionario(Pessoa):
    salario = models.DecimalField('Salário', max_digits=8, decimal_places=2, help_text='Salário base do funcionário')
    foto = models.ImageField('Foto', null=True, blank=True)

    class Meta:
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'
        ordering = [Upper('nome')]