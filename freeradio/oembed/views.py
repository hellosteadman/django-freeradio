from django.core.urlresolvers import resolve
from django.http.response import HttpResponseBadRequest
from django.utils import six
from django.views.generic.base import View
import json

if six.PY2:
    from urlparse import urlparse, urljoin
else:
    from urllib.parse import urlparse, urljoin


class OEmbedProviderView(View):
    def get(self, request):
        url = request.GET.get('url')
        if not url:
            return HttpResponseBadRequest(
                json.dumps(
                    {
                        'error': u'url parameter missing'
                    }
                ),
                content_type='text/javascript'
            )

        urlparts = urlparse(url)
        path = urlparts.path
        resolved = resolve(path)

        kwargs = resolved.kwargs
        kwargs['as_oembed_html'] = True
        return resolved.func(request, *resolved.args, **kwargs)
