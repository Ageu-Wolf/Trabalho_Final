
from django.db import models
from django.db.models.functions import Upper
from Clientes.models import Cliente

class Carro(models.Model):
    clientes = models.ManyToManyField(
        Cliente,
        blank=True,
        verbose_name='Clientes Associados',
        related_name='carros_pertencentes'
    )
    placa = models.CharField('Placa', max_length=10, help_text='Placa do veículo (Ex: ABC-1234)', unique=True, primary_key=True)
    modelo = models.CharField('Modelo', max_length=100, help_text='Modelo do carro (Ex: Fusca, Uno)')
    cor = models.CharField('Cor', max_length=50, help_text='Cor do carro (Ex: Vermelho, Prata)')

    class Meta:
        verbose_name = 'Carro'
        verbose_name_plural = 'Carros'
        ordering = [Upper('modelo'), 'placa']
        permissions = (
            ('visualizar_carro', 'Pode visualizar a lista e detalhes de carros'),
            ('cadastrar_carro', 'Pode adicionar novos carros'),
            ('editar_carro', 'Pode editar carros existentes'),
            ('deletar_carro', 'Pode excluir carros'),
        )

    def __str__(self):
        return f"{self.modelo} - {self.placa}"