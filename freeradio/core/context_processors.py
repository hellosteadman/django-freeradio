from django.conf import settings as site_settings
from django.contrib.sites.models import Site
from constance import config
from .models import Feature


def settings(request):
    site = Site.objects.get_current()

    return {
        'RADIO_STREAM_URL': config.RADIO_STREAM_URL,
        'RADIO_NOWPLAYING_URL': config.RADIO_NOWPLAYING_URL,
        'GOOGLE_ANALYTICS_ID': config.GOOGLE_ANALYTICS_ID,
        'FACEBOOK_APP_ID': config.FACEBOOK_APP_ID,
        'SITE': site,
        'OFFAIR_TEXT': config.OFFAIR_TEXT,
        'HOME_TITLE': config.HOME_TITLE,
        'HOME_INTRO': config.HOME_INTRO,
        'IOS_APP_URL': config.IOS_APP_URL,
        'ANDROID_APP_URL': config.ANDROID_APP_URL,
        'MAILCHIMP_FORM_URL': config.MAILCHIMP_FORM_URL
    }


def home(request):
    return {
        'homepage_features': Feature.objects.all()[:5]
    }
