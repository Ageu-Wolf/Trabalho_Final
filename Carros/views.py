from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db.models import RestrictedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView
from django.contrib import messages
from .forms import CarroForm
from .models import Carro
from django.views.generic import CreateView, DetailView
class CarrosView(LoginRequiredMixin,ListView):
    model = Carro
    template_name = 'carros.html'
    context_object_name = 'carros'
    permission_required = 'carros.visualizar_carro'
    permission_denied_message = 'Você não tem permissão para visualizar a lista de carros.'

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


class CarroAddView(LoginRequiredMixin,SuccessMessageMixin, CreateView):
    model = Carro
    form_class = CarroForm
    template_name = 'carro_form.html'
    success_url = reverse_lazy('carros')
    success_message = 'Carro cadastrado com sucesso.'
    permission_required = 'carros.cadastrar_carro'
    permission_denied_message = 'Você não tem permissão para cadastrar novos carros.'


class CarroUpdateView(LoginRequiredMixin,SuccessMessageMixin, UpdateView):
    model = Carro
    form_class = CarroForm
    template_name = 'carro_form.html'
    success_url = reverse_lazy('carros')
    success_message = 'Carro atualizado com sucesso!'
    permission_required = 'carros.editar_carro'
    permission_denied_message = 'Você não tem permissão para editar este carro.'

class CarroDeleteView(LoginRequiredMixin,SuccessMessageMixin, DeleteView):
    model = Carro
    template_name = 'carro_apagar.html'
    success_url = reverse_lazy('carros')
    success_message = 'Carro deletado com sucesso!'
    permission_required = 'carros.deletar_carro'
    permission_denied_message = 'Você não tem permissão para deletar carros.'
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        try:
            self.object.delete()

            return super().post(request, *args, **kwargs)

        except RestrictedError:

            messages.error(
                request,
                f"Não foi possível excluir o carro (Placa: {self.object.placa}). Existem registros de estacionamento vinculados a ele. Remova ou edite esses registros primeiro."
            )
            return redirect(self.success_url)

class CarroDetailView(LoginRequiredMixin,DetailView):
    model = Carro
    template_name = 'carro_detalhe.html'
    context_object_name = 'carro'
    permission_required = 'carros.visualizar_carro'
    permission_denied_message = 'Você não tem permissão para ver detalhes de carros.'

