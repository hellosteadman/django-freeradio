from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^playlist/$', PlaylistView.as_view(), name='playlist')
]
