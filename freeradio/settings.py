from django.core.urlresolvers import reverse
from django.utils import six
import os
import dj_database_url

if six.PY2:
    from urlparse import urlparse, urljoin
else:
    from urllib.parse import urlparse, urljoin


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', True) and True or False
ALLOWED_HOSTS = ['*']
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'collectfast',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    's3direct',
    'storages',
    'sorl.thumbnail',
    'markdown_deux',
    'django_rq',
    'taggit',
    'ckeditor',
    'ckeditor_uploader',
    'constance',
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
        'dsn': os.getenv('SENTRY_DSN')
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
SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT') == 'true'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
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
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'freeradio'
    }
}

DATABASES['default'].update(
    dj_database_url.config(conn_max_age=500)
)

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
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
    'django.contrib.staticfiles.finders.AppDirectoriesFinder'
)

if not DEBUG:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    STATICFILES_STORAGE = 'freeradio.core.storages.S3StaticStorage'

REDIS_URL = os.getenv('REDIS_URL', 'redis://127.0.0.1:6379/')
REDIS_URL_PARTS = urlparse(REDIS_URL)

RQ_QUEUES = {
    'default': {
        'URL': REDIS_URL
    }
}

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_S3_BUCKET')
AWS_S3_CUSTOM_DOMAIN = os.getenv('AWS_S3_CUSTOM_DOMAIN') or (
    's3-eu-west-1.amazonaws.com/%s' % AWS_STORAGE_BUCKET_NAME
)

AWS_PRELOAD_METADATA = True
AWS_QUERYSTRING_AUTH = False

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = DEBUG and '/media/' or '//%s/uploads/' % AWS_S3_CUSTOM_DOMAIN
STATIC_URL = DEBUG and '/static/' or ('//%s/static/' % AWS_S3_CUSTOM_DOMAIN)
SITE_ID = os.getenv('SITE_ID')
S3DIRECT_REGION = 'eu-west-1'

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
            os.getenv('REDIS_URL', 'redis://localhost:6379/0')
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
    },
    'collectfast': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'collectfast'
    }
}

COLLECTFAST_CACHE = 'collectfast'

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

MIXCLOUD_USERNAME = os.getenv('MIXCLOUD_USERNAME')
OEMBED_ENDPOINTS = (
    (
        (
            'http://flickr.com/photos/*',
            'https://flickr.com/photos/*'
        ),
        'https://www.flickr.com/services/oembed/'
    ),
    (
        (
            'http://vimeo\.com/*',
            'https://vimeo\.com/*'
        ),
        'https://www.vimeo.com/api/oembed.json'
    ),
    (
        (
            'http://youtube.com/*',
            'https://youtube.com/*',
            'http://www.youtube.com/*',
            'https://www.youtube.com/*'
        ),
        'https://www.youtube.com/oembed'
    ),
    (
        (
            'http://www.mixcloud.com/*',
            'https://www.mixcloud.com/*'
        ),
        'https://www.mixcloud.com/oembed/'
    ),
    (
        (
            'http://www.soundcloud.com/*',
            'https://www.soundcloud.com/*',
            'http://soundcloud.com/*',
            'https://soundcloud.com/*',
        ),
        'https://soundcloud.com/oembed?maxheight=81'
    )
)

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


CONSTANCE_CONFIG = {
    'OFFAIR_TEXT': (
        'Our local music mix',
        'What to display when there is no live show'
    ),
    'HOME_TITLE': (
        '{{ HOME_TITLE }}',
        'Homepage heading text'
    ),
    'HOME_INTRO': (
        '{{ HOME_INTRO }}',
        'Home intro text'
    ),
    'IOS_APP_URL': (
        '{{ IOS_APP_URL }}',
        'iOS app URL'
    ),
    'ANDROID_APP_URL': (
        '{{ ANDROID_APP_URL }}',
        'Android app URL'
    ),
    'RADIO_STREAM_URL': (
        os.getenv('RADIO_STREAM_URL'),
        'Shoutcast stream URL'
    ),
    'RADIO_NOWPLAYING_URL': (
        os.getenv('RADIO_NOWPLAYING_URL'),
        'Now-playing XML URL'
    ),
    'GOOGLE_ANALYTICS_ID': (
        os.getenv('GOOGLE_ANALYTICS_ID'),
        'Google Analytics ID'
    ),
    'FACEBOOK_APP_ID': (
        os.getenv('FACEBOOK_APP_ID'),
        'Facebook app ID'
    )
}
