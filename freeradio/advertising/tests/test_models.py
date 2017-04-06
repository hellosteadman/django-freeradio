from django.test import TestCase
from ..models import Advert


class AdvertTests(TestCase):
    def test_str(self):
        advert = Advert(name=u'New advert')
        self.assertEqual(str(advert), u'New advert')
