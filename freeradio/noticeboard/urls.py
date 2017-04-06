from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^noticeboard\.css', StylesheetView.as_view(), name='stylesheet')
]
