from django.views.generic.base import TemplateView
from .settings import SIZES


class StylesheetView(TemplateView):
    content_type = 'text/css'
    template_name = 'noticeboard/sizes.css'

    def get_context_data(self, **kwargs):
        return {
            'sizes': SIZES
        }
