from django.template import Library
from ..models import Advert

register = Library()


@register.inclusion_tag('advertisement/region.inc.html')
def ad_region(region_name):
    return {
        'ads': Advert.objects.filter(
            placements__region=region_name
        ).order_by(
            'placements__order',
        ).distinct()
    }
