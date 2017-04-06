from django.db.models import Manager
from . import get_oembed_content, guess_oembed_content


class ResourceManager(Manager):
    def create_resource(self, url, width, endpoint, fmt):
        return self.create(
            url=url,
            width=width,
            html=get_oembed_content(url, endpoint, fmt, width)
        )

    def guess_resource(self, url, width):
        try:
            return self.get(url=url, width=width)
        except self.model.DoesNotExist:
            html = guess_oembed_content(url, width)

            if html:
                return self.create(
                    url=url,
                    width=width,
                    html=html
                )
