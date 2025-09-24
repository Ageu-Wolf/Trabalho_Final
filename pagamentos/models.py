from django.db import models
from estacionamentos.models import Estacionamento

class Pagamento(Estacionamento):
    tipo = models.CharField(max_length=3)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_hora = models.DateTimeField()
    referencia = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Pagamento {self.id} - Estacionamento {self.id}"
