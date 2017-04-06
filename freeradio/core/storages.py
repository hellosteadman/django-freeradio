from __future__ import absolute_import
from storages.backends.s3boto import S3BotoStorage


class S3StaticStorage(S3BotoStorage):
    location = 'static'


class S3MediaStorage(S3BotoStorage):
    location = 'media'
