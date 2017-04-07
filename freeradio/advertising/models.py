from django.db import models
from django_filepicker.models import FPFileField
from .settings import REGIONS


class Advert(models.Model):
    name = models.CharField(max_length=100)
    image = FPFileField(
        mimetypes=('image/*',),
        null=True,
        blank=True
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
