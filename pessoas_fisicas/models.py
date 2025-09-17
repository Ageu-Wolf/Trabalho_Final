from django.db import models

from Pessoas.models import Pessoa


class PessoaFisica(Pessoa):
    cpf = models.CharField(max_length=11, unique=True, verbose_name='CPF')

    class Meta:
        verbose_name='Pessoa_Fisica'
        verbose_name_plural='Pessoas_Fisicas'

    def __str__(self):
        return self.nome
