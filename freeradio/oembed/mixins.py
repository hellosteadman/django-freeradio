from django.http.response import HttpResponse
from django.core.urlresolvers import reverse
from django.utils.http import urlquote
import json


class OEmbedResourceMixin(object):
    def get(self, request, *args, **kwargs):
        if kwargs.get('as_oembed_html') or self.kwargs.get('as_oembed_html'):
            width = request.GET.get('width')
            maxwidth = request.GET.get('maxwidth')
            obj = self.get_object()
            html, width, height = obj.get_oembed_html(
                width=width,
                maxwidth=maxwidth
            )

            return HttpResponse(
                json.dumps(
                    {
                        'type': 'video',
                        'html': html,
                        'width': width,
                        'height': height,
                        'version': '1.0',
                        'title': str(obj)
                    }
                ),
                content_type='text/javascript'
            )

        response = super(OEmbedResourceMixin, self).get(
            request, *args, **kwargs
        )

        if kwargs.get('embedded') or self.kwargs.get('embedded'):
            response['Access-Control-Allow-Origin'] = '*'

        return response

    def get_context_data(self, *args, **kwargs):
        context = super(OEmbedResourceMixin, self).get_context_data(
            *args,
            **kwargs
        )

        context['oembed_url'] = 'https://%s%s?url=%s' % (
            self.request.get_host(),
            reverse('oembed_provider'),
            urlquote(
                'https://%s%s' % (
                    self.request.get_host(),
                    self.object.get_absolute_url()
                )
            )
        )

        return context
