from django.db import models

class Pagamento(Estacionamento):
    tipo = models.CharField(max_length=3)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_hora = models.DateTimeField()
    referencia = models.CharField(max_length=100, null=True, blank=True)
    estacionamento = models.ForeignKey(related_name="pagamentos")

    def __str__(self):
        return self.estacionamento
