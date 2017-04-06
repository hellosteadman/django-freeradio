from django.conf.urls import url
from .views import OEmbedProviderView


urlpatterns = [
    url(r'^$', OEmbedProviderView.as_view(), name='oembed_provider')
]
