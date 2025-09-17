from django.db import models

from django.db import models

class Pessoa(models.Model):
    numero = models.Integer(max_length=4)
    status = models.CharField(max_length=15, verbose_name='Status')

    class Meta:
        verbose_name = 'vaga'
        verbose_name_plural = 'Vagas'

    def __str__(self):
        return self.numero

