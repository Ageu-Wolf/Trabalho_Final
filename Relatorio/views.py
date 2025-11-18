from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from Vagas.models import Estacionamento

class RelatorioListView(LoginRequiredMixin,ListView):
    model = Estacionamento

    template_name = 'relatorio.html'
    context_object_name = 'relatorios'
    permission_required = 'relatorio.visualizar_relatorio'
    permission_denied_message = 'Você não tem permissão para acessar os relatórios de movimentação.'

    def get_queryset(self):
        return Estacionamento.objects.filter(estado='CONCLUIDO').order_by('-data_hora_saida')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        for registro in context['relatorios']:
            duration = registro.tempo_permanencia

            if duration:
                total_segundos = int(duration.total_seconds())

                horas = total_segundos // 3600
                minutos = (total_segundos % 3600) // 60
                segundos = total_segundos % 60

                duracao_formatada = f"{horas:02d}:{minutos:02d}:{segundos:02d}"
            else:
                duracao_formatada = "N/A"

            registro.duracao_formatada = duracao_formatada
            # Calcular totais e somas para exibição (opcional, mas útil para relatórios)
        context['total_ganhos'] = sum(r.pagamento for r in context['relatorios'] if r.pagamento is not None)
        context['total_carros_concluidos'] = context['relatorios'].count()
        return context