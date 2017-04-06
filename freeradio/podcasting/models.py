from dateutil.parser import parse as parse_date
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.safestring import mark_safe
from django.utils.html import escape
from ckeditor_uploader.fields import RichTextUploadingField
import feedparser


class Series(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=30, unique=True)
    subtitle = models.CharField(max_length=150)
    author = models.CharField(max_length=50)
    email = models.EmailField(max_length=255)
    public = models.BooleanField(default=True)
    banner = models.ImageField(
        upload_to='podcasts',
        max_length=255
    )

    presenters = models.ManyToManyField(
        'talent.Presenter',
        through='SeriesPresenter'
    )

    url = models.URLField(u'feed URL', max_length=255)
    description = models.TextField(null=True, blank=True)
    artwork = models.ImageField(
        max_length=255,
        upload_to='podcasts'
    )

    def __str__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('podcasting:series', [self.slug])

    @property
    def widget_url(self):
        url = self.url
        if url.endswith('/'):
            url = url[:-1]

        urlparts = url.split('/')
        return '%s/subscribe.js' % (
            '/'.join(urlparts[:-1])
        )

    def check_for_episodes(self):
        feed = feedparser.parse(self.url)
        for entry in feed.entries:
            try:
                episode = self.episodes.get(guid=entry.guid)
            except Episode.DoesNotExist:
                episode = Episode(
                    series=self,
                    guid=entry.guid,
                    slug=slugify(entry.title)
                )

            episode.title = entry.title
            episode.url = entry.link
            episode.published = parse_date(entry.published)
            for content in entry.content:
                if content.type == 'text/html':
                    episode.description = content.value

            episode.save()

    def get_presenters_display(self):
        presenter_names = list(
            self.seriespresenter_set.values_list(
                'presenter__name',
                flat=True
            )
        )

        if len(presenter_names) > 2:
            return '%s and %s' % (
                ', '.join(presenter_names[0:-1]),
                presenter_names[-1]
            )

        return ' and '.join(presenter_names)

    class Meta:
        ordering = ('slug',)


class SeriesPresenter(models.Model):
    series = models.ForeignKey(Series)
    presenter = models.ForeignKey(
        'talent.Presenter',
        related_name='podcasts'
    )

    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return u'%s - %s' % (self.series.name, self.presenter.name)

    class Meta:
        unique_together = ('presenter', 'series')
        ordering = ('order',)
        db_table = 'podcasting_series_presenters'


class SubscriptionLink(models.Model):
    series = models.ForeignKey(Series, related_name='subscription_links')
    store = models.CharField(
        max_length=20,
        choices=(
            ('itunes', u'iTunes'),
            ('stitcher', u'Stitcher'),
            ('pcast', u'Pocket Casts'),
            ('overcast', u'Overcast')
        )
    )

    url = models.URLField(u'URL', max_length=255)

    def __str__(self):
        return self.get_store_display()

    class Meta:
        ordering = ('store',)
        unique_together = ('store', 'series')


class Episode(models.Model):
    series = models.ForeignKey(Series, related_name='episodes')
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    url = models.URLField(u'player URL', max_length=255)
    guid = models.CharField(max_length=255, unique=True)
    published = models.DateTimeField(null=True, blank=True)
    description = RichTextUploadingField(null=True, blank=True)

    def __str__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('podcasting:episode', [self.series.slug, self.slug])

    def player(self):
        return mark_safe(
            '<iframe src="%s" width="100%%" height="150" '
            'frameborder="0"></iframe>' % (
                escape(self.url + 'embed/')
            )
        )

    def get_download_url(self):
        return '%sdownload.mp3' % self.url

    class Meta:
        ordering = ('-published',)
