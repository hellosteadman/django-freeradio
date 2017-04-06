from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.utils import timezone
from hashlib import md5
from datetime import timedelta


class Artist(models.Model):
    name = models.CharField(max_length=50)
    photo = models.ImageField(
        max_length=255,
        upload_to='music',
        null=True,
        blank=True
    )

    url = models.URLField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Track(models.Model):
    artist = models.ForeignKey(Artist, related_name='tracks')
    title = models.CharField(max_length=100)
    artwork = models.ImageField(
        max_length=255,
        upload_to='music',
        null=True,
        blank=True
    )

    notes = models.TextField(null=True, blank=True)
    sample_url = models.URLField(
        u'sample URL',
        max_length=255,
        null=True,
        blank=True
    )

    purchase_url = models.URLField(
        u'purchase URL',
        max_length=255,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title

    def render_sample(self):
        cachekey = 'rendered_media_%s' % md5(self.sample_url).hexdigest()
        rendered = cache.get(cachekey)

        if rendered is None:
            rendered = (
                u'<a class="btn btn-default" href="%s" '
                'target="_blank">%s</a>' % (
                    self.sample_url,
                    _(u'Hear a sample')
                )
            )
            cache.set(cachekey, rendered, 60 * 60 * 24)

        return mark_safe(rendered)

    class Meta:
        ordering = ('title',)


class Playlist(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=30, unique=True)
    tracks = models.ManyToManyField(Track, through='PlaylistTrack')

    def __str__(self):
        return self.name

    def tracks_recently_added(self):
        last_week = timezone.localtime(timezone.now()) - timedelta(days=14)
        return self.playlisttrack_set.select_related().filter(
            added__gte=last_week
        )

    def tracks_not_recently_added(self):
        last_week = timezone.localtime(timezone.now()) - timedelta(days=14)
        return self.playlisttrack_set.select_related().filter(
            added__lt=last_week
        )


class PlaylistTrack(models.Model):
    playlist = models.ForeignKey(Playlist)
    track = models.ForeignKey(Track, related_name='playlists')
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return u'%s - %s' % (self.playlist.name, self.track.title)

    @property
    def image(self):
        return self.track.artwork or self.track.artist.photo

    class Meta:
        ordering = ('track__artist__name', 'track__title')
        unique_together = ('track', 'playlist')
        db_table = 'music_playlist_tracks'
