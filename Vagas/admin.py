from django.contrib import admin
from .models import Vaga, Carro, Cliente, Estacionamento
# Adicione todos os seus modelos aqui!

# 1. Registrar o modelo Vaga
admin.site.register(Vaga)

# 2. Registrar o modelo Estacionamento (onde criamos o registro)
admin.site.register(Estacionamento)

# 3. Registrar outros modelos se necessário (Carro, Cliente, etc.)
admin.site.register(Carro)
admin.site.register(Cliente)