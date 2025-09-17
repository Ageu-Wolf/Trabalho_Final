from django.db import models

from django.db import models

class Preco(models.Model):
    valor_hora = models.FloatField(max_length=10, verbose_name='Valor Hora')
    valor_pernoite = models.FloatField(max_length=10, verbose_name='Valor Pernoite')
    valor_afiliado = models.FloatField(max_length=10, verbose_name='Valor Afiliado')

    class Meta:
        verbose_name = 'Preço'
        verbose_name_plural = 'Preços'

    def __str__(self):
        return self.valor_hora

