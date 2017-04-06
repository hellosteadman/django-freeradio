from django.db import models
from django.core.cache import cache
from ckeditor.fields import RichTextField
from .helpers import upload_presenter_photo


class Presenter(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=30, unique=True)
    short_name = models.CharField(max_length=50)

    user = models.OneToOneField(
        'auth.User',
        related_name='presenter_profile',
        null=True,
        blank=True
    )

    photo = models.ImageField(
        upload_to='upload_presenter_photo',
        max_length=255,
        null=True,
        blank=True
    )

    bio = RichTextField(null=True, blank=True)
    alumnus = models.BooleanField(default=False)
    twitter_username = models.CharField(max_length=30, null=True, blank=True)
    facebook_username = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

    def banner_colour(self):
        if not self.photo:
            return

        cachekey = 'presenter_%d_banner_colour' % self.pk
        cached = cache.get(cachekey)

        if cached is None:
            from colorthief import ColorThief
            photo = self.photo.storage.open(self.photo.name)
            thief = ColorThief(photo)
            cached = thief.get_color(quality=1)
            cache.set(cachekey, cached, 60 * 60 * 24)

        return cached

    def banner_darkness(self):
        colour = self.banner_colour()
        if colour is None:
            return False

        red, blue, green = self.banner_colour()
        red, blue, green = (
            float(red) / 255.0 * 100.0,
            float(blue) / 255.0 * 100.0,
            float(green) / 255.0 * 100.0
        )

        return round((red + blue + green) / 300.0, 1)

    def banner_lightness(self):
        return abs(1.0 - self.banner_darkness())

    @models.permalink
    def get_absolute_url(self):
        return ('talent:presenter', [self.slug])

    def regular_programmes(self):
        from ..traffic.models import Programme

        return Programme.objects.filter(
            presenters=self
        ).exclude(
            recurrence=-1
        )

    def programme_updates(self):
        from ..traffic.models import Update

        return Update.objects.filter(
            programme__presenters=self
        )

    class Meta:
        ordering = ('name',)
