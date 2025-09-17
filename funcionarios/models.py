from django.db import models

from django.db import models
from stdimage import StdImageField

from pessoas_fisicas.models import PessoaFisica


class Funcionario(PessoaFisica):
    foto = StdImageField('foto',upload_to='funcionarios',delete_orphans=True,null=True,blank=True)
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    data_admissao = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = 'Funcionario'
        verbose_name_plural = 'Funcionarios'

    def __str__(self):
        return self.nome

