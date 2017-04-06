from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^blog/$', PostsView.as_view(), name='posts'),
    url(
        r'^blog/(?P<slug>[\w-]+)/$',
        PostView.as_view(),
        name='post'
    )
]
