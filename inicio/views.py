# inicio/views.py

from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = "inicio.html" # Deve ser o nome do seu arquivo HTML