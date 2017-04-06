from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^presenters/$', PresentersView.as_view(), name='presenters'),
    url(
        r'^presenters/(?P<slug>[\w-]+)/$',
        PresenterView.as_view(),
        name='presenter'
    )
]
