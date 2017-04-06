from ..api import APIEndpointBase
from .models import Series
from sorl.thumbnail import get_thumbnail


class SeriesEndpoint(APIEndpointBase):
    def get(self):
        def t(thumb, size):
            if not thumb:
                return

            thumbnail = get_thumbnail(thumb, size)
            if thumbnail:
                return thumbnail.url

        for series in Series.objects.all():
            yield {
                'name': series.name,
                'subtitle': series.subtitle,
                'description': series.description,
                'logo': t(series.artwork, '300x300'),
                'banner': t(series.banner, '828x465'),
                'presenters': series.get_presenters_display()
            }
