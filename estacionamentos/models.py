from django.db import models
from precos.models import Preco


class Estacionamento(models.Model):
    data_hora_entrada = models.DateTimeField()
    data_hora_saida = models.DateTimeField(null=True, blank=True)

    funcionario = models.ForeignKey(
        "funcionarios.Funcionario",
        on_delete=models.CASCADE,
        related_name="estacionamentos_funcionario"  # nome único para o reverso
    )
    cliente = models.ForeignKey(
        "pessoas_fisicas.PessoaFisica",
        on_delete=models.CASCADE,
        related_name="estacionamentos_cliente"  # nome único para o reverso
    )
    vaga = models.ForeignKey(
        "vagas.Vaga",
        on_delete=models.CASCADE
    )

    pernoite = models.BooleanField(default=False)
    relatorio = models.TextField(null=True, blank=True)
    pagamento_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    preco = models.ForeignKey(Preco, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Estacionamento {self.id}"
