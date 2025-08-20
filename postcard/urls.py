from tempfile import template

from django.urls import path
from django.views.generic import TemplateView
from .views import visualizar_postal, enviar_postal

urlpatterns = [
    path('', TemplateView.as_view(template_name='postcard/index.html'), name='index'),
    path('enviar', enviar_postal, name='enviar'),
    path('preview', visualizar_postal, name='visualizar'),
]