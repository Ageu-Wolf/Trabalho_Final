from django.db import models
from django.utils import timezone
import uuid 

class Relatorio(models.Model):
    TIPO_CHOICES = [
        ('PIX', 'Pix'),
        ('CREDITO', 'Cartão de Crédito'),
        ('DEBITO', 'Cartão de Débito'),
        ('DINHEIRO', 'Dinheiro'),
    ]

    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_hora = models.DateTimeField(default=timezone.now) 
    referencia = models.CharField(max_length=255, unique=True, default=uuid.uuid4)

    class Meta:
        verbose_name = "Relatório de Pagamento"
        verbose_name_plural = "Relatórios de Pagamentos"
        permissions = (
            ('visualizar_relatorio', 'Pode visualizar relatórios de movimentação e ganhos'),
            ('exportar_relatorio', 'Pode exportar relatórios para arquivo'),
        )

    def __str__(self):
        return f"Relatório Ref: {self.referencia} - Valor: R$ {self.valor}"