from django.conf import settings as site_settings


REGIONS = getattr(site_settings, 'ADVERTISEMENT_REGIONS', {})
