from django.db import models

class Carro(models.Model):
    modelo = models.CharField(max_length=100)
    cor = models.CharField(max_length=20)
    placa = models.CharField(max_length=12, unique=True, verbose_name='Placa')

    class Meta:
        verbose_name = 'Carro'
        verbose_name_plural = 'Carros'

    def __str__(self):
        return self.modelo

