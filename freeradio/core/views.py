from django.views.generic.base import TemplateView
from .mixins import BootstrapMixin


class HomeView(BootstrapMixin, TemplateView):
    template_name = 'core/home.html'
    body_classes = ('core', 'home')
    menu_selection = 'core:home'
    title_parts = ['The alternative sound for Birmingham']


class PlayerView(BootstrapMixin, TemplateView):
    template_name = 'core/player.html'
    body_classes = ('core', 'player')
    title_parts = ['Player']
