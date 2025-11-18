# inicio/urls.py
from django.contrib.auth.views import PasswordChangeView, LogoutView, LoginView
from django.urls import path, reverse_lazy
from .views import IndexView # Certifique-se que IndexView existe e está correta

urlpatterns = [
    # A rota interna pode ser vazia, pois o caminho raiz ('') já foi definido no arquivo principal
    path('', IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(template_name='login.html', extra_context={'titulo': 'Autenticação'}),
         name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('alterar_senha/',
         PasswordChangeView.as_view(template_name='login.html', extra_context={'titulo': 'Alterar senha'},
                                    success_url=reverse_lazy('index')), name='alterar_senha'),
]