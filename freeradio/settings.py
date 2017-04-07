import environ
import dj_database_url

from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.utils import six

if six.PY2:
    from urlparse import urlparse, urljoin
else:
    from urllib.parse import urlparse, urljoin

env = environ.Env()
env.read_env('.env')

BASE_DIR = environ.Path(__file__) - 2
SECRET_KEY = env('DJANGO_SECRET_KEY')
DEBUG = env.bool('DJANGO_DEBUG', False)
ALLOWED_HOSTS = ['*']
INSTALLED_APPS = [
    'suit',
    'suit_redactor',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    's3direct',
    'storages',
    'sorl.thumbnail',
    'markdown_deux',
    'django_rq',
    'taggit',
    'constance',
    'constance.backends.database',
    'sass_processor',
    'freeradio.core',
    'freeradio.advertising',
    'freeradio.talent',
    'freeradio.traffic',
    'freeradio.podcasting',
    'freeradio.music',
    'freeradio.noticeboard',
    'freeradio.blog',
    'freeradio.oembed'
]

if not DEBUG:
    RAVEN_CONFIG = {
        'dsn': env('SENTRY_DSN', default='')
    }

    INSTALLED_APPS += ('raven.contrib.django.raven_compat',)

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]

ROOT_URLCONF = 'freeradio.urls'
SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', False)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR.path('templates')
        ],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'freeradio.core.context_processors.settings',
                'freeradio.core.context_processors.home',
                'freeradio.traffic.context_processors.traffic',
                'freeradio.noticeboard.context_processors.noticeboard'
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader'
            ],
            'debug': DEBUG
        },
    },
]

WSGI_APPLICATION = 'freeradio.wsgi.application'
DATABASES = {
    'default': env.db(
        'DATABASE_URL',
        default='sqlite:///%s' % BASE_DIR.path('freeradio.sqlite')
    )
}

DATABASES['default'].update(
    dj_database_url.config(conn_max_age=500)
)

# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'UserAttributeSimilarityValidator'
        )
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.MinimumLengthValidator'
        )
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.CommonPasswordValidator'
        )
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.NumericPasswordValidator'
        )
    }
]

LANGUAGE_CODE = 'en-gb'
TIME_ZONE = 'Europe/London'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'sass_processor.finders.CssFinder'
)

STATICFILES_DIRS = [
    BASE_DIR.path('freeradio/static/')()
]

if (
    env('DROPBOX_OAUTH2_TOKEN', default='') and
    env('DROPBOX_ROOT_PATH', default='')
):
    DEFAULT_FILE_STORAGE = 'storages.backends.dropbox.DropboxStorage'
    STATICFILES_STORAGE = 'freeradio.core.dropbox.DropboxStaticStorage'
    DROPBOX_OAUTH2_TOKEN = env('DROPBOX_OAUTH2_TOKEN', default='')
    DROPBOX_ROOT_PATH = env('DROPBOX_ROOT_PATH', default='')
elif env('AWS_S3_BUCKET', default=''):
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    STATICFILES_STORAGE = 'freeradio.core.storages.S3StaticStorage'
    S3DIRECT_REGION = 'eu-west-1'
    AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID', default='')
    AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY', default='')
    AWS_STORAGE_BUCKET_NAME = env('AWS_S3_BUCKET', default='')
    AWS_S3_CUSTOM_DOMAIN = env('AWS_S3_CUSTOM_DOMAIN', default='') or (
        's3-eu-west-1.amazonaws.com/%s' % AWS_STORAGE_BUCKET_NAME
    )

    AWS_PRELOAD_METADATA = True
    AWS_QUERYSTRING_AUTH = False
elif not DEBUG:
    raise ImproperlyConfigured(
        'Either a DROPBOX_OAUTH2_TOKEN or AWS_S3_BUCKET must be defined.'
    )

REDIS_URL = env('REDIS_URL', default='redis://127.0.0.1:6379/')
REDIS_URL_PARTS = urlparse(REDIS_URL)

RQ_QUEUES = {
    'default': {
        'URL': REDIS_URL
    }
}

MEDIA_ROOT = BASE_DIR.path('media')()
STATIC_ROOT = BASE_DIR.path('staticfiles')()
MEDIA_URL = DEBUG and '/media/' or '//%s/uploads/' % AWS_S3_CUSTOM_DOMAIN
STATIC_URL = DEBUG and '/static/' or ('//%s/static/' % AWS_S3_CUSTOM_DOMAIN)
SITE_ID = env.int('SITE_ID', 1)

S3DIRECT_DESTINATIONS = {
    'podcast_episodes': {
        'key': 'podcasts',
        'allowed': ['audio/mpeg', 'audio/mpeg3', 'audio/x-mpeg-3'],
    }
}

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': [
            env('REDIS_URL', default='redis://127.0.0.1:6379')
        ],
        'OPTIONS': {
            'DB': 0,
            'CONNECTION_POOL_CLASS': 'redis.BlockingConnectionPool',
            'CONNECTION_POOL_CLASS_KWARGS': {
                'max_connections': 50,
                'timeout': 20
            },
            'MAX_CONNECTIONS': 1000,
            'PICKLE_VERSION': -1
        },
        'KEY_PREFIX': 'cache'
    }
}

NOTICEBOARD_MODELS = (
    (
        'blog.Post',
        {
            'subtitle': u'New to the blog',
            'title': str,
            'image_field': 'featured_image',
            'description_field': 'excerpt',
            'cta_text': u'Read more',
            'date_field': 'published'
        }
    ),
    (
        'music.PlaylistTrack',
        {
            'subtitle': lambda o: u'New track on %s' % str(o.playlist),
            'title': lambda o: u'%s - %s' % (o.track.artist, o.track),
            'image_field': 'image',
            'cta_text': u'Check it out',
            'cta_url': lambda o: (
                o.track.purchase_url or
                o.track.artist.url or
                reverse('music:playlist')
            ),
            'stickiness': 5,
            'date_field': 'added'
        }
    ),
    (
        'podcasting.Series',
        {
            'subtitle': u'New podcast',
            'title': str,
            'description_field': 'subtitle',
            'cta_text': u'Hear the first episode',
            'stickiness': 7,
            'image_field': 'artwork'
        }
    ),
    (
        'podcasting.Episode',
        {
            'subtitle': lambda o: o.series.name,
            'title': str,
            'cta_text': u'Listen now',
            'stickiness': 4,
            'image': lambda o: o.series.artwork,
            'date_field': 'published'
        }
    ),
    (
        'traffic.Update',
        {
            'subtitle': lambda o: (
                o.kind == 'episode' and 'Listen again' or 'Show news'
            ),
            'title': lambda o: str(o.programme),
            'description_field': 'description',
            'image_field': 'programme.logo',
            'cta_text': lambda o: (
                o.kind == 'episode' and 'Listen' or 'Read more'
            ),
            'cta_url': lambda o: reverse(
                'traffic:programme',
                args=[o.programme.slug]
            ),
            'date_field': 'date'
        }
    )
)

CKEDITOR_UPLOAD_PATH = 'uploads'
CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'minimalist',
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_Advanced': [
            {
                'name': 'basicstyles',
                'items': [
                    'Format',
                    'Bold',
                    'Italic',
                    'Subscript',
                    'Superscript',
                    '-',
                    'RemoveFormat'
                ]
            },
            {
                'name': 'paragraph',
                'items': [
                    'NumberedList',
                    'BulletedList',
                    '-',
                    'Outdent',
                    'Indent',
                    '-',
                    'Blockquote'
                ]
            },
            {
                'name': 'links',
                'items': [
                    'Link',
                    'Unlink',
                    'Anchor'
                ]
            },
            {
                'name': 'insert',
                'items': [
                    'Image',
                    'HorizontalRule',
                    'Smiley',
                    'SpecialChar',
                ]
            }
        ],
        'toolbar': 'Advanced',
        'tabSpaces': 4,
        'extraPlugins': ','.join(
            [
                'autogrow',
                'widget',
                'lineutils',
                'clipboard',
                'dialog',
                'dialogui',
                'elementspath'
            ]
        )
    }
}

THUMBNAIL_DEBUG = DEBUG
THUMBNAIL_KVSTORE = 'sorl.thumbnail.kvstores.redis_kvstore.KVStore'
THUMBNAIL_REDIS_PASSWORD = REDIS_URL_PARTS.password
THUMBNAIL_REDIS_HOST = REDIS_URL_PARTS.hostname
THUMBNAIL_REDIS_PORT = REDIS_URL_PARTS.port

NOTICEBOARD_SIZES = {
    'blog.post': {
        768: [2, 2]
    },
    'music.playlisttrack': {
        768: [1, 2]
    },
    'podcasting.series': {
        768: [3, 2],
        1200: [2, 2]
    },
    'podcasting.episode': {
        768: [3, 1],
        1200: [2, 1]
    },
    'traffic.update': {
        768: [3, 1],
        1200: [1, 1]
    }
}

ADVERTISEMENT_REGIONS = {
    'home_01': 'Homepage (before Features)',
    'home_01': 'Homepage (after Features)',
    'sidebar': 'Sidebar'
}


CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
CONSTANCE_CONFIG = {
    'OFFAIR_TEXT': (
        'Our local music mix',
        'What to display when there is no live show'
    ),
    'HOME_TITLE': (
        'Welcome to Django Free Radio',
        'Homepage heading text'
    ),
    'HOME_INTRO': (
        'You can change this content in the admin site',
        'Home intro text'
    ),
    'IOS_APP_URL': (
        'https://itunes.apple.com/gb/app/brum-radio/id1218461799?mt=8',
        'iOS app URL'
    ),
    'ANDROID_APP_URL': (
        'https://play.google.com/store/apps/details?id=com.ionicframework.combrumradio701094',
        'Android app URL'
    ),
    'RADIO_STREAM_URL': (
        env(
            'RADIO_STREAM_URL',
            default='http://uk3.internet-radio.com:11168/stream'
        ),
        'Shoutcast stream URL'
    ),
    'RADIO_NOWPLAYING_URL': (
        env(
            'RADIO_NOWPLAYING_URL',
            default='https://control.internet-radio.com:2199/external/rpc.php?m=streaminfo.get&username=brumradio&charset=&mountpoint=&rid=brumradio'
        ),
        'Now-playing XML URL'
    ),
    'GOOGLE_ANALYTICS_ID': (
        env('GOOGLE_ANALYTICS_ID', default=''),
        'Google Analytics ID'
    ),
    'FACEBOOK_APP_ID': (
        env('FACEBOOK_APP_ID', default=''),
        'Facebook app ID'
    ),
    'MIXCLOUD_USERNAME': (
        env('MIXCLOUD_USERNAME', default='brumradio'),
        'MixCloud username'
    ),
    'MAILCHIMP_FORM_URL': (
        env(
            'MAILCHIMP_FORM_URL',
            default='//freeradio.us5.list-manage.com/subscribe/post?u=ff5d7e986a83ed1a1e1de6c27&amp;id=19d2b7f483'
        ),
        'MailChimp subscription form URL'
    )
}
