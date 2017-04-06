from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http.response import HttpResponse, HttpResponsePermanentRedirect
from django.views.generic.base import TemplateView, View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import Series, Episode
from ..core.mixins import BootstrapMixin


class PodcastsView(BootstrapMixin, ListView):
    model = Series
    body_classes = ('podcasting', 'podcasts')
    menu_selection = 'podcasting:podcasts'
    title_parts = ['Podcasts']


class SeriesView(BootstrapMixin, DetailView):
    model = Series
    body_classes = ('podcasting', 'series')
    menu_selection = 'podcasting:series'

    def get_title_parts(self):
        yield self.object.name
        yield 'Podcasts'

    def get_social_image(self):
        return self.object.artwork

    def get_social_description(self):
        return self.object.subtitle

    def get_context_data(self, **kwargs):
        context = super(SeriesView, self).get_context_data(**kwargs)
        rightnow = timezone.localtime(timezone.now())
        episodes = kwargs['object'].episodes.filter(
            published__lte=rightnow
        )

        paginator = Paginator(episodes, 10)

        try:
            page = paginator.page(self.request.GET.get('page'))
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)

        context['episodes'] = page
        return context


class EpisodeView(BootstrapMixin, DetailView):
    model = Episode
    body_classes = ('podcasting', 'episode')
    menu_selection = 'podcasting:episode'

    def get_title_parts(self):
        yield self.object.title
        yield self.object.series.name
        yield 'Podcasts'

    def get_social_image(self):
        return self.object.series.artwork

    def get_social_description(self):
        return self.object.series.subtitle

    def get_context_data(self, **kwargs):
        context = super(EpisodeView, self).get_context_data(**kwargs)
        context['series'] = kwargs['object'].series
        return context


class SeriesRSSView(View):
    def get(self, request, slug):
        series = get_object_or_404(Series, slug=slug)
        return HttpResponsePermanentRedirect(series.url)


class PodcastWebhookView(View):
    def get(self, request, slug):
        series = get_object_or_404(Series, slug=slug)
        series.check_for_episodes()
        return HttpResponse('OK', content_type='text/plain')
