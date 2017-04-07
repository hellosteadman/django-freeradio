from django.db import models
from django_filepicker.models import FPFileField


class Feature(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=255, null=True, blank=True)
    image = FPFileField(
        mimetypes=('image/*',),
        null=True,
        blank=True
    )

    url = models.URLField(u'URL', max_length=255)
    ordering = models.PositiveIntegerField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('ordering',)
