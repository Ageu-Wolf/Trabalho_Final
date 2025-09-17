from django.db import models
from Pessoas.models import Pessoa


class PessoaJuridica(Pessoa):
    cnpj = models.CharField(max_length=18, unique=True, verbose_name='CNPJ')

    class Meta:
        verbose_name='Pessoa_Juridica'
        verbose_name_plural='Pessoas_Juridicas'

    def __str__(self):
        return super().nome

