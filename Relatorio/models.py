# Vagas/models.py (Substituindo a classe Pagamento)
from django.db import models
from django.utils import timezone
import uuid 

class Relatorio(models.Model):
    # Tipos de Pagamento
    TIPO_CHOICES = [
        ('PIX', 'Pix'),
        ('CREDITO', 'Cartão de Crédito'),
        ('DEBITO', 'Cartão de Débito'),
        ('DINHEIRO', 'Dinheiro'),
    ]

    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    # Valor é o valor final recebido
    valor = models.DecimalField(max_digits=10, decimal_places=2) 
    data_hora = models.DateTimeField(default=timezone.now) 
    # Referência única da transação no relatório
    referencia = models.CharField(max_length=255, unique=True, default=uuid.uuid4) 

    class Meta:
        verbose_name = "Relatório de Pagamento"
        verbose_name_plural = "Relatórios de Pagamentos"

    def __str__(self):
        return f"Relatório Ref: {self.referencia} - Valor: R$ {self.valor}"