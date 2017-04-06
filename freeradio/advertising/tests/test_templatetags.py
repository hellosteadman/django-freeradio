from django.test import TestCase
from django.template import Template, Context
from ..models import Advert


class AdRegionTests(TestCase):
    def setUp(self):
        ad_one = Advert.objects.create(name='Test one', html='<p>Test</p>')
        ad_one.placements.create(region='sidebar', order=10)
        ad_one.placements.create(region='homepage')

        ad_two = Advert.objects.create(name='Test two', html='<p>Test</p>')
        ad_two.placements.create(region='sidebar', order=20)

    def test_ad_region(self):
        html = '{% load advertising %}{% ad_region \'sidebar\' %}'
        self.assertEqual(
            Template(html).render(Context()),
            '<div class="bcwfujtfnfou"><p>Test</p></div>'
            '<div class="bcwfujtfnfou"><p>Test</p></div>\n'
        )
