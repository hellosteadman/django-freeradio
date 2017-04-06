from django.db import models
from .settings import REGIONS
from .helpers import upload_advert_image


class Advert(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(
        max_length=255,
        null=True,
        blank=True,
        upload_to=upload_advert_image
    )

    url = models.URLField(u'URL', max_length=255, null=True, blank=True)
    html = models.TextField(u'HTML', null=True, blank=True)

    def __str__(self):
        return self.name


class Placement(models.Model):
    advert = models.ForeignKey(Advert, related_name='placements')
    region = models.CharField(max_length=30, choices=REGIONS.items())
    order = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('region', 'advert')
        ordering = ('order',)
