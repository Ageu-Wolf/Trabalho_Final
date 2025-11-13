from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Funcionario
from .forms import FuncionarioModelForm
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q

class FuncionarioListView(ListView):
    model = Funcionario
    template_name = 'funcionarios.html'
    context_object_name = 'funcionarios'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        busca = self.request.GET.get('buscar')

        if busca:

            queryset = queryset.filter(
                Q(nome__icontains=busca)
            )
        return queryset

class FuncionarioCreateView(SuccessMessageMixin, CreateView):
    model = Funcionario
    form_class = FuncionarioModelForm
    template_name = 'funcionario_form.html'
    success_url = reverse_lazy('funcionarios')
    success_message = "Funcionário '%(nome)s' cadastrado com sucesso!"

class FuncionarioUpdateView(SuccessMessageMixin, UpdateView):
    model = Funcionario
    form_class = FuncionarioModelForm
    template_name = 'funcionario_form.html'
    success_url = reverse_lazy('funcionarios')
    success_message = "Funcionário '%(nome)s' editado com sucesso!"





class FuncionarioDeleteView(DeleteView):
    model = Funcionario
    template_name = 'funcionario_deletar.html'
    success_url = reverse_lazy('funcionarios')