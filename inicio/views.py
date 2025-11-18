# inicio/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

class IndexView(LoginRequiredMixin,TemplateView):
    template_name = "inicio.html" # Deve ser o nome do seu arquivo HTML