from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.utils import timezone
from .models import Presenter
from ..core.mixins import BootstrapMixin


class PresentersView(BootstrapMixin, ListView):
    model = Presenter
    body_classes = ('talent', 'presenters')
    menu_selection = 'talent:presenters'
    title_parts = ['Presenters']

    def get_context_data(self, **kwargs):
        context = super(PresentersView, self).get_context_data(**kwargs)
        context['with_photos'] = context['object_list'].exclude(
            photo=None
        ).exclude(
            photo=''
        ).filter(
            alumnus=False
        )

        q = Q(photo=None) | Q(photo='')
        context['without_photos'] = context['object_list'].filter(
            alumnus=False
        ).filter(q)

        del context['object_list']
        return context


class PresenterView(BootstrapMixin, DetailView):
    model = Presenter
    body_classes = ('talent', 'presenter')
    menu_selection = 'talent:presenter'

    def get_title_parts(self):
        yield self.object.name
        yield 'Presenters'

    def get_social_image(self):
        return self.object.photo

    def get_context_data(self, **kwargs):
        context = super(PresenterView, self).get_context_data(**kwargs)
        rightnow = timezone.localtime(timezone.now())
        updates = kwargs['object'].programme_updates().filter(
            date__lte=rightnow
        )

        paginator = Paginator(updates, 10)

        try:
            page = paginator.page(self.request.GET.get('page'))
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)

        context['updates'] = page
        return context
