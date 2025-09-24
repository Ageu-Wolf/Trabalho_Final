from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .forms import CarroModelForm
from .models import Carro

class FornecedoresView(ListView):
    model = Carro
    template_name = 'fornecedores.html'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(FornecedoresView, self).get_queryset()

        if buscar:
            qs = qs.filter(nome__icontains=buscar)

        if qs.count() > 0:
            paginator = Paginator(qs, 1)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            return messages.info(self.request, 'Não existem fornecedores cadastrados.')

class FornecedorAddView(SuccessMessageMixin, CreateView):
    model = Carro
    form_class = CarroModelForm
    template_name = 'fornecedor_form.html'
    success_url = reverse_lazy('fornecedores')
    success_message = "Fornecedor cadastrado com sucesso!"

class FornecedorUpdateView(SuccessMessageMixin, UpdateView):
    model = Carro
    form_class = CarroModelForm
    template_name = 'fornecedor_form.html'
    success_url = reverse_lazy('fornecedores')
    success_message = "Fornecedor atualizado com sucesso!"

class FornecedorDeleteView(SuccessMessageMixin, DeleteView):
    model = Carro
    template_name = 'fornecedor_apagar.html'
    success_url = reverse_lazy('fornecedores')
    success_message = 'Fornecedor deletado com sucesso!'