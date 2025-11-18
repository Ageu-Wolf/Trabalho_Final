from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db.models import RestrictedError
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Cliente
from .forms import ClienteModelForm

class ClientesView(LoginRequiredMixin,ListView):
    model = Cliente
    template_name = 'clientes.html'
    permission_required = 'clientes.visualizar_cliente'
    permission_denied_message = 'Você não tem permissão para visualizar a lista de clientes.'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super().get_queryset()

        if buscar:
            qs = qs.filter(nome__icontains=buscar)

        if qs.exists():
            paginator = Paginator(qs, 10)  # ajustei para 10 por página
            return paginator.get_page(self.request.GET.get('page'))
        else:
            messages.info(self.request, 'Não existem clientes cadastrados.')
            return qs.none()

class ClienteAddView(LoginRequiredMixin,SuccessMessageMixin, CreateView):
    model = Cliente
    form_class = ClienteModelForm
    template_name = 'cliente_form.html'
    success_url = reverse_lazy('clientes')
    success_message = 'Cliente cadastrado com sucesso.'
    permission_required = 'clientes.cadastrar_cliente'
    permission_denied_message = 'Você não tem permissão para cadastrar novos clientes.'

class ClienteUpdateView(LoginRequiredMixin,SuccessMessageMixin, UpdateView):
    model = Cliente
    form_class = ClienteModelForm
    template_name = 'cliente_form.html'
    success_url = reverse_lazy('clientes')
    success_message = 'Cliente atualizado com sucesso.'
    permission_required = 'clientes.editar_cliente'
    permission_denied_message = 'Você não tem permissão para editar este cliente.'

class ClienteDeleteView(LoginRequiredMixin,SuccessMessageMixin, DeleteView):
    model = Cliente
    template_name = 'cliente_apagar.html'
    success_url = reverse_lazy('clientes')
    success_message = 'Cliente excluído com sucesso.'
    permission_required = 'clientes.deletar_cliente'
    permission_denied_message = 'Você não tem permissão para excluir clientes.'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        try:
            self.object.delete()
            return super().post(request, *args, **kwargs)

        except RestrictedError:

            messages.error(
                request,
                f"Não foi possível excluir o cliente. Existem registros de estacionamento vinculados a ele ({self.object.pk}). Remova ou edite os registros primeiro."
            )

            # ✅ CORREÇÃO: Use o atalho 'redirect' para retornar um objeto HttpResponseRedirect
            return redirect(self.success_url)
