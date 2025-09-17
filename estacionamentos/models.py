from django.db import models

from precos.models import Preco
from funcionarios.models import Funcionario


class Estacionamento(models.Model):
    data_hora_entrada = models.DateTimeField()
    data_hora_saida = models.DateTimeField(null=True, blank=True)

    funcionario = models.ForeignKey(
        "Funcionario",
    )
    cliente = models.ForeignKey(
        "PessoaFisica",
    )
    vaga = models.ForeignKey(
        "Vaga"
    )

    pernoite = models.BooleanField(default=False)
    relatorio = models.TextField(null=True, blank=True)
    pagamento_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    preco = models.ForeignKey(Preco, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return
