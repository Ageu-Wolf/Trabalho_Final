from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, DetailView, View
from django.views.generic import CreateView
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import transaction
from Relatorio.models import Relatorio
from .forms import EstacionamentoEntradaForm, PagamentoForm
from .models import Vaga, Estacionamento


class VagasView(LoginRequiredMixin,TemplateView):
    template_name = 'vagas.html'
    permission_required = 'estacionamento.visualizar_vagas'
    permission_denied_message = 'Você não tem permissão para visualizar as Vagas.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Conta as vagas
        total_vagas = 100
        context['total_vagas'] = total_vagas
        context['vagas_ocupadas'] = Vaga.objects.filter(status='O').count()
        context['vagas_livres'] = total_vagas - context['vagas_ocupadas']
        context['vagas_manutencao'] = Vaga.objects.filter(status='M').count()

        context['registros_ativos'] = Estacionamento.objects.filter(
            estado='ATIVO'
        ).select_related('vaga', 'carro')

        return context

class EstacionamentoCreateView(LoginRequiredMixin,CreateView):
    model = Estacionamento
    form_class = EstacionamentoEntradaForm
    template_name = 'estacionamento_entrada.html'
    success_url = reverse_lazy('Vagas')
    permission_required = 'estacionamento.registrar_entrada'
    permission_denied_message = 'Você não tem permissão para registrar uma nova Entrada.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vagas_livres_count'] = Vaga.objects.filter(status='L').count()
        return context

    def form_valid(self, form):
        vaga_disponivel = Vaga.objects.filter(status='L').first()

        if not vaga_disponivel:
            form.add_error(None, "Desculpe, não há vagas livres para registrar a entrada.")
            return self.form_invalid(form)

        carro_a_estacionar = form.cleaned_data.get('carro')
        vaga_disponivel.status = 'O'
        vaga_disponivel.carro_estacionado = carro_a_estacionar
        vaga_disponivel.save()

        form.instance.vaga = vaga_disponivel

        return super().form_valid(form)


class CalculoPagamentoView(LoginRequiredMixin,DetailView):
    model = Estacionamento
    template_name = 'estacionamento_saida.html'
    context_object_name = 'registro'
    permission_required = 'estacionamento.finalizar_saida'
    permission_denied_message = 'Você não tem permissão para calcular a Saída.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        registro = self.object

        data_saida, duracao, valor_total_base = registro.calcular_valor_total()

        context['form'] = PagamentoForm()

        context['data_saida_estimada'] = data_saida
        context['tempo_permanencia'] = duracao
        context['valor_total'] = valor_total_base

        return context


class ConfirmacaoPagamentoView(LoginRequiredMixin,View):
    success_url = reverse_lazy('Vagas')
    permission_required = 'estacionamento.finalizar_saida'
    permission_denied_message = 'Você não tem permissão para confirmar o Pagamento/Saída.'

    def post(self, request, pk):
        registro = get_object_or_404(Estacionamento, pk=pk, estado='ATIVO')
        form = PagamentoForm(request.POST)

        if form.is_valid():
            metodo_selecionado = form.cleaned_data['metodo_pagamento']

            try:
                data_saida, duracao, valor_total_base = registro.calcular_valor_total()
                valor_total_final = registro.aplicar_regra_pagamento(valor_total_base, metodo_selecionado)

                with transaction.atomic():

                    novo_relatorio = Relatorio.objects.create(
                        tipo=metodo_selecionado,
                        valor=valor_total_final,
                    )

                    # 2b. Salva o método de pagamento usado ANTES de finalizar
                    # Note: O campo 'pagamento' no Estacionamento será atualizado no finalize_saida
                    registro.metodo_pagamento_final = metodo_selecionado
                    registro.save(update_fields=['metodo_pagamento_final'])

                    registro.finalizar_saida_e_liberar_vaga(
                        data_saida,
                        duracao,
                        valor_total_final,
                        novo_relatorio
                    )

                messages.success(request,
                                 f"Pagamento de R$ {valor_total_final:.2f} via {metodo_selecionado} registrado (Relatório ID: {novo_relatorio.id}) e vaga liberada para {registro.carro.placa}.")

            except Exception as e:
                messages.error(request, f"Erro ao finalizar pagamento: {e}")
                return redirect('calculo_pagamento', pk=pk)  # Volta para a tela de cálculo em caso de falha

        else:
            messages.error(request, "Método de pagamento não selecionado. Por favor, tente novamente.")
            return redirect('calculo_pagamento', pk=pk)

        return redirect(self.success_url)