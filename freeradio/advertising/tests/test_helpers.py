from django.test import TestCase
from ..helpers import upload_advert_image
import time


class MockInstance(object):
    pass


class UploadAdvertImageTests(TestCase):
    def test_upload_advert_image(self):
        old_time = time.time
        time.time = lambda: 1473330369.667939

        self.assertEqual(
            upload_advert_image(MockInstance(), 'test.jpg'),
            'bcwfujtfnfou/3457dc953561de.jpg'
        )

        time.time = old_time
