from django.template import Library
from django.conf import settings
from ..models import Resource
from .. import URL_REGEX, get_oembed_endpoint, sandbox_iframe
import re

SANDBOX = getattr(settings, 'OEMBED_SANDBOX', True)
WIDTH = getattr(settings, 'OEMBED_WIDTH', 640)

register = Library()


@register.filter()
def oembed(value, width=WIDTH):
    if not value:
        return u''

    if '<p' not in value and '</p>' not in value:
        value = '<p>%s</p>' % value

    match = URL_REGEX.search(value)
    while match is not None and match.end() <= len(value):
        start = match.start()
        end = match.end()
        groups = match.groups()
        replaced = False

        if len(groups) > 0:
            url = groups[0]
            inner = '<p><a href="%(url)s">%(url)s</a></p>' % {
                'url': url
            }

            endpoint, fmt = get_oembed_endpoint(url)
            if endpoint and fmt:
                try:
                    resource = Resource.objects.get(
                        url=url,
                        width=width
                    )
                except Resource.DoesNotExist:
                    try:
                        resource = Resource.objects.create_resource(
                            url, width, endpoint, fmt
                        )
                    except:
                        if settings.DEBUG:
                            raise
                    else:
                        inner = resource.html
                        replaced = True
                else:
                    inner = resource.html
                    replaced = True
        else:
            inner = ''

        if not replaced:
            try:
                resource = Resource.objects.guess_resource(url, width)
            except:
                if settings.DEBUG:
                    raise
            else:
                if resource:
                    inner = resource.html
                    if SANDBOX:
                        inner = sandbox_iframe(inner)

                    replaced = True

        value = value[:start] + inner + value[end:]
        match = URL_REGEX.search(value, start + len(inner))

    return value
