from django.views.generic import TemplateView, DetailView, View
from django.views.generic import CreateView
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import transaction

from Relatorio.models import Relatorio
from .forms import EstacionamentoEntradaForm, PagamentoForm
from .models import Vaga, Estacionamento


class VagasView(TemplateView):
    """ Mostra a visão geral das vagas e os carros estacionados. """
    template_name = 'vagas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Conta as vagas
        total_vagas = 100
        context['total_vagas'] = total_vagas
        context['vagas_ocupadas'] = Vaga.objects.filter(status='O').count()
        context['vagas_livres'] = total_vagas - context['vagas_ocupadas']
        context['vagas_manutencao'] = Vaga.objects.filter(status='M').count()

        # Lista os carros ativos (select_related torna a busca mais rápida)
        context['registros_ativos'] = Estacionamento.objects.filter(
            estado='ATIVO'
        ).select_related('vaga', 'carro')

        return context

class EstacionamentoCreateView(CreateView):
    """ Registra a entrada de um veículo e ocupa a primeira vaga livre. """
    model = Estacionamento
    form_class = EstacionamentoEntradaForm
    template_name = 'estacionamento_entrada.html'
    success_url = reverse_lazy('Vagas')

    def get_context_data(self, **kwargs):
        """ Adiciona a contagem de vagas livres para exibição no formulário. """
        context = super().get_context_data(**kwargs)
        context['vagas_livres_count'] = Vaga.objects.filter(status='L').count()
        return context

    def form_valid(self, form):
        # 1. Encontra a primeira vaga livre
        vaga_disponivel = Vaga.objects.filter(status='L').first()

        if not vaga_disponivel:
            form.add_error(None, "Desculpe, não há vagas livres para registrar a entrada.")
            return self.form_invalid(form)

        # 2. Ocupa a vaga e associa o carro
        carro_a_estacionar = form.cleaned_data.get('carro')
        vaga_disponivel.status = 'O'  # Altera para 'O' (Ocupada)
        vaga_disponivel.carro_estacionado = carro_a_estacionar
        vaga_disponivel.save()

        # 3. Associa a vaga ao novo registro de Estacionamento
        form.instance.vaga = vaga_disponivel

        # 4. Salva o registro de Estacionamento
        return super().form_valid(form)


class CalculoPagamentoView(DetailView):
    """ Exibe o cálculo de horas, o valor base e o formulário de pagamento. """
    model = Estacionamento
    template_name = 'estacionamento_saida.html'
    context_object_name = 'registro'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        registro = self.object

        # 1. Chama o método do Modelo para calcular o tempo e o valor base
        data_saida, duracao, valor_total_base = registro.calcular_valor_total()

        # 2. Adiciona o formulário de pagamento (sem JS)
        context['form'] = PagamentoForm()

        # 3. Passa os dados para o template
        context['data_saida_estimada'] = data_saida
        context['tempo_permanencia'] = duracao
        context['valor_total'] = valor_total_base

        return context


class ConfirmacaoPagamentoView(View):
    """ Processa o pagamento, aplica a taxa/desconto, CRIA O RELATÓRIO e finaliza o registro. """
    success_url = reverse_lazy('Vagas')

    def post(self, request, pk):
        registro = get_object_or_404(Estacionamento, pk=pk, estado='ATIVO')
        form = PagamentoForm(request.POST)

        if form.is_valid():
            metodo_selecionado = form.cleaned_data['metodo_pagamento']

            try:
                # 1. Calcula o valor base e final
                data_saida, duracao, valor_total_base = registro.calcular_valor_total()
                valor_total_final = registro.aplicar_regra_pagamento(valor_total_base, metodo_selecionado)

                # 2. Garante que o registro, vaga e relatório sejam salvos JUNTOS
                with transaction.atomic():

                    # 2a. CRIA O REGISTRO DE RELATÓRIO 🚨 NOVO PASSO 🚨
                    novo_relatorio = Relatorio.objects.create(
                        tipo=metodo_selecionado,
                        valor=valor_total_final,
                        # data_hora e referencia são automáticos
                    )

                    # 2b. Salva o método de pagamento usado ANTES de finalizar
                    # Note: O campo 'pagamento' no Estacionamento será atualizado no finalize_saida
                    registro.metodo_pagamento_final = metodo_selecionado
                    registro.save(update_fields=['metodo_pagamento_final'])

                    # 2c. Finaliza Estacionamento e libera Vaga
                    # Passa a instância do Relatório como argumento
                    registro.finalizar_saida_e_liberar_vaga(
                        data_saida,
                        duracao,
                        valor_total_final,
                        novo_relatorio  # <== ARGUMENTO ADICIONAL: INSTÂNCIA DO RELATÓRIO
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