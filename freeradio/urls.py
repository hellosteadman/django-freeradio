from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from s3direct import urls as s3direct_urls
from django_rq import urls as rq_urls
from ckeditor_uploader import urls as ckeditor_uploader_urls
from .core import urls as core_urls
from .noticeboard import urls as noticeboard_urls
from .traffic import urls as traffic_urls
from .talent import urls as talent_urls
from .podcasting import urls as podcasting_urls
from .blog import urls as blog_urls
from .music import urls as music_urls


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^django-rq/', include(rq_urls)),
    url(r'^s3direct/', include(s3direct_urls)),
    url(r'^ckeditor/', include(ckeditor_uploader_urls)),
    url(r'^', include(traffic_urls, namespace='traffic')),
    url(r'^', include(talent_urls, namespace='talent')),
    url(r'^', include(podcasting_urls, namespace='podcasting')),
    url(r'^', include(blog_urls, namespace='blog')),
    url(r'^', include(music_urls, namespace='music')),
    url(r'^', include(core_urls, namespace='core')),
    url(r'^', include(noticeboard_urls, namespace='noticeboard')),
]

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    from django.views.static import serve

    urlpatterns += staticfiles_urlpatterns() + [
        url(
            r'^media/(?P<path>.*)$', serve,
            {
                'document_root': settings.MEDIA_ROOT
            }
        )
    ]
