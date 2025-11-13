from django.views.generic import ListView

from Vagas.models import Estacionamento
from .models import Relatorio

class RelatorioListView(ListView):
    """ Exibe a lista de todos os registros de pagamento finalizados. """
    model = Estacionamento

    # 2. Seu template está correto, mas o nome do contexto era 'relatorios'
    template_name = 'relatorio.html'
    context_object_name = 'relatorios'

    # Sobrescreva get_queryset para aplicar o filtro de "pago/finalizado"
    def get_queryset(self):
        # Filtra apenas os registros que têm o estado marcado como 'CONCLUIDO'
        return Estacionamento.objects.filter(estado='CONCLUIDO').order_by('-data_hora_saida')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Iterar sobre cada registro no queryset para formatar o tempo
        for registro in context['relatorios']:
            # Pega o objeto timedelta (tempo_permanencia)
            duration = registro.tempo_permanencia

            # Garante que a duração existe
            if duration:
                # Converte o timedelta para segundos totais (como float) e depois para int
                total_segundos = int(duration.total_seconds())

                # Calcula Horas, Minutos e Segundos
                horas = total_segundos // 3600
                minutos = (total_segundos % 3600) // 60
                segundos = total_segundos % 60

                # Formata a string como HH:MM:SS
                duracao_formatada = f"{horas:02d}:{minutos:02d}:{segundos:02d}"
            else:
                duracao_formatada = "N/A"

            # CRIA UM NOVO ATRIBUTO no objeto chamado 'duracao_formatada'
            registro.duracao_formatada = duracao_formatada

        return context