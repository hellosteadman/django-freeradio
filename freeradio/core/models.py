from django.db import models


class Feature(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(
        max_length=255,
        upload_to='homepage/features',
        null=True,
        blank=True
    )

    url = models.URLField(u'URL', max_length=255)
    ordering = models.PositiveIntegerField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('ordering',)
