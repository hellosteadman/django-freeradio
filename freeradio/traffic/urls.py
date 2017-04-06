from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^schedule/$', ScheduleView.as_view(), name='schedule'),
    url(
        r'^schedule/(?P<day>mon|tue|wed|thu|fri|sat|sun)/$',
        ScheduleView.as_view(),
        name='schedule_day'
    ),
    url(r'^shows/$', ProgrammeListView.as_view(), name='programmes'),
    url(r'^shows/(?P<slug>[\w-]+)/$', ProgrammeView.as_view(), name='programme')
]
