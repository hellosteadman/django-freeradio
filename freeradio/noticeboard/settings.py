from django.conf import settings as site_settings

SIZES = getattr(site_settings, 'NOTICEBOARD_SIZES', {})
