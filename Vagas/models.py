from django.db import models
from django.utils import timezone
from datetime import timedelta
from Carros.models import Carro
from Clientes.models import Cliente
from funcionarios.models import Funcionario
import math
from Relatorio.models import Relatorio


class Vaga(models.Model):

    STATUS_CHOICES = (
        ('L', 'Livre'),
        ('O', 'Ocupada'),
        ('M', 'Manutenção'),
    )

    numero = models.CharField('Número da Vaga', max_length=10, unique=True)


    status = models.CharField('Status', max_length=1, choices=STATUS_CHOICES, default='L')


    carro_estacionado = models.OneToOneField(
        Carro,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Carro Estacionado'
    )

    class Meta:
        verbose_name = 'Vaga'
        verbose_name_plural = 'Vagas'
        ordering = ['numero']

    def __str__(self):
        return f"Vaga {self.numero} ({self.get_status_display()})"

    @property
    def esta_livre(self):
        return self.status == 'L'


class Estacionamento(models.Model):
    relatorio_final = models.OneToOneField(
        'Relatorio.Relatorio',  # <-- Nova referência de string
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='registro_estacionamento'
    )
    METODOS_PAGAMENTO = [
        ('DINHEIRO', 'Dinheiro'),
        ('DEBITO', 'Débito'),
        ('CREDITO', 'Crédito'),
        ('PIX', 'Pix'),
    ]
    metodo_pagamento_final = models.CharField(
        max_length=10,
        choices=METODOS_PAGAMENTO,
        null=True,
        blank=True
    )

    PERIODOS = (
        ('HORA', 'Por Hora'),
        ('DIARIA', 'Diária'),
        ('MENSAL', 'Mensal'),
    )


    STATUS_REGISTRO = (
        ('ATIVO', 'Ativo (Veículo no Local)'),
        ('CONCLUIDO', 'Concluído (Saída Registrada)'),
    )

    data_hora_entrada = models.DateTimeField(default=timezone.now, verbose_name="Entrada")
    data_hora_saida = models.DateTimeField(null=True, blank=True, verbose_name="Saída")

    estado = models.CharField(
        max_length=50,
        choices=STATUS_REGISTRO,
        default='ATIVO',
        verbose_name="Status da Sessão"
    )


    carro = models.ForeignKey(
        Carro,
        on_delete=models.RESTRICT,
        verbose_name="Veículo Estacionado"
    )

    funcionario = models.ForeignKey(
        Funcionario,
        on_delete=models.RESTRICT,
        verbose_name="Funcionário (Entrada)"
    )

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.RESTRICT,
        null=True, blank=True,
        verbose_name="Cliente/Mensalista"
    )

    vaga = models.ForeignKey(
        Vaga,
        on_delete=models.RESTRICT,
        verbose_name="Vaga Ocupada"
    )


    periodo_estimado = models.CharField(
        max_length=50,
        choices=PERIODOS,
        default='HORA',
        verbose_name="Período de Cobrança Estimado"
    )

    pagamento = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True, blank=True,
        verbose_name="Valor Total Pago"
    )

    tempo_permanencia = models.DurationField(null=True, blank=True, verbose_name="Tempo de Permanência")

    relatorio = models.TextField(max_length=500, null=True, blank=True, verbose_name="Relatório / Observações")

    class Meta:
        verbose_name = "Registro de Estacionamento"
        verbose_name_plural = "Registros de Estacionamento"

    def __str__(self):
        return f"{self.carro.placa} na Vaga {self.vaga.numero} | {self.estado}"

    def calcular_permanencia(self):
        if self.data_hora_saida and self.data_hora_entrada:
            return self.data_hora_saida - self.data_hora_entrada
        return timedelta()

    def aplicar_regra_pagamento(self, valor_base, metodo):
        valor_final = valor_base
        taxa_credito = 0.05  # 5%
        desconto_pix = 0.05  # 5%

        if metodo == 'CREDITO':
            # Aplica taxa de 5%
            valor_final = valor_base * (1 + taxa_credito)
        elif metodo == 'PIX':
            # Aplica desconto de 5%
            valor_final = valor_base * (1 - desconto_pix)

        # Retorna o valor final (já arredondado para duas casas)
        return round(valor_final, 2)

    def calcular_valor_total(self, preco_por_hora=5.00):
        """
        Calcula o tempo de permanência e o valor base (sem taxa/desconto).
        """
        data_saida = timezone.now()
        duracao_timedelta = data_saida - self.data_hora_entrada

        # 1. Calcula a duração formatada (para display)
        total_segundos = int(duracao_timedelta.total_seconds())
        horas = total_segundos // 3600
        minutos = (total_segundos % 3600) // 60
        duracao_formatada = f"{horas}h {minutos}m"

        # 2. Calcula o valor base (arredondando a hora para cima)
        horas_float = duracao_timedelta.total_seconds() / 3600
        horas_cobradas = math.ceil(horas_float)
        valor_total_base = round(horas_cobradas * preco_por_hora, 2)

        # Retorna o data_saida, o timedelta e o valor base
        return data_saida, duracao_timedelta, valor_total_base

    def finalizar_saida_e_liberar_vaga(self, data_saida, duracao_timedelta, valor_final,relatorio_instance):
        """
        FINALIZA o registro e LIBERA a vaga.
        """
        # 1. Atualiza o registro de estacionamento
        self.data_hora_saida = data_saida
        self.tempo_permanencia = duracao_timedelta  # Salva o objeto timedelta
        self.pagamento = valor_final
        self.estado = 'CONCLUIDO'  # Ou 'FINALIZADO' dependendo do seu choice
        self.relatorio_final = relatorio_instance

        # O campo 'metodo_pagamento_final' deve ter sido setado na View antes de chamar este método!

        # 2. Libera a vaga
        vaga = self.vaga
        vaga.status = 'L'  # L = Livre
        vaga.carro_estacionado = None
        vaga.save()

        self.save()