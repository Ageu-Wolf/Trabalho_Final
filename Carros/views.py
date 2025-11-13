from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView
from django.contrib import messages
from .forms import CarroForm
from .models import Carro
from django.views.generic import CreateView, DetailView
class CarrosView(ListView):
    model = Carro
    template_name = 'carros.html'
    context_object_name = 'carros'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(CarrosView, self).get_queryset()

        if buscar:
            qs = qs.filter(modelo__icontains=buscar)

        if qs.exists():
            paginator = Paginator(qs, 5)
            page = self.request.GET.get('page')
            return paginator.get_page(page)
        else:
            messages.info(self.request, 'Não existe nenhum carro cadastrado.')
            return qs.none()


class CarroAddView(SuccessMessageMixin, CreateView):
    model = Carro
    form_class = CarroForm
    template_name = 'carro_form.html'
    success_url = reverse_lazy('carros')
    success_message = 'Carro cadastrado com sucesso.'


class CarroUpdateView(SuccessMessageMixin, UpdateView):
    model = Carro
    form_class = CarroForm
    template_name = 'carro_form.html'
    success_url = reverse_lazy('carros')
    success_message = 'Carro atualizado com sucesso!'


class CarroDeleteView(SuccessMessageMixin, DeleteView):
    model = Carro
    template_name = 'carro_apagar.html'
    success_url = reverse_lazy('carros')
    success_message = 'Carro deletado com sucesso!'

class CarroDetailView(DetailView):
    model = Carro
    template_name = 'carro_detalhe.html'
    context_object_name = 'carro'