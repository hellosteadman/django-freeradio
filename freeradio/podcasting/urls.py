from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^podcasts/$', PodcastsView.as_view(), name='podcasts'),
    url(
        r'^webhooks/podcasts/(?P<slug>[\w-]+)/$',
        PodcastWebhookView.as_view(), name='podcast_webhook'
    ),
    url(
        r'^podcasts/(?P<slug>[\w-]+)/$',
        SeriesView.as_view(),
        name='series'
    ),
    url(
        r'^podcasts/(?P<slug>[\w-]+)/rss/$',
        SeriesRSSView.as_view(),
        name='rss'
    ),
    url(
        r'^podcasts/(?P<series__slug>[\w-]+)/(?P<slug>[\w-]+)/$',
        EpisodeView.as_view(),
        name='episode'
    )
]
