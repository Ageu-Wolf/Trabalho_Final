from django.db import models

class Vaga(models.Model):
    numero = models.IntegerField()
    status = models.CharField(max_length=15, verbose_name='Status')

    class Meta:
        verbose_name = 'vaga'
        verbose_name_plural = 'vagas'

    def __str__(self):
        return str(self.numero)
