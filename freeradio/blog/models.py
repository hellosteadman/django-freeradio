from django.db import models
from django.utils.html import strip_tags
from django.template.defaultfilters import truncatewords
from taggit.managers import TaggableManager
from django_filepicker.models import FPFileField
from html2text import html2text
from markdown2 import markdown


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'categories'


class Blogger(models.Model):
    name = models.CharField(max_length=100)
    biography = models.TextField(null=True, blank=True)
    user = models.OneToOneField(
        'auth.User',
        related_name='blogger_profile',
        null=True,
        blank=True
    )

    photo = FPFileField(
        mimetypes=('image/*',),
        null=True,
        blank=True
    )

    twitter_username = models.CharField(max_length=30, null=True, blank=True)
    facebook_username = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Post(models.Model):
    title = models.CharField(max_length=140)
    slug = models.SlugField(max_length=30, unique=True)
    body = models.TextField()
    excerpt = models.TextField(null=True, blank=True)
    author = models.ForeignKey('auth.User', related_name='user')
    blogger = models.ForeignKey(
        Blogger,
        related_name='posts',
        null=True,
        blank=True
    )

    created = models.DateTimeField(auto_now_add=True)
    published = models.DateTimeField(null=True, blank=True)
    featured_image = FPFileField(
        mimetypes=('images/*',),
        null=True,
        blank=True
    )

    categories = models.ManyToManyField(Category, related_name='posts')
    tags = TaggableManager()

    def __str__(self):
        return self.title

    def get_excerpt(self):
        if self.excerpt:
            return self.excerpt

        text = html2text(self.body, bodywidth=10000)
        lines = []

        for line in text.splitlines():
            if not line or not line.strip():
                continue

            if line[0] in ('#', '-', '>'):
                continue

            line = strip_tags(markdown(line))
            if not line or not line.strip():
                continue

            lines.append(line)
            if len(line.split(' ')) >= 20:
                break

        return truncatewords(' '.join(lines), 20)

    @models.permalink
    def get_absolute_url(self):
        return ('blog:post', [self.slug])

    class Meta:
        ordering = ('-published',)
        get_latest_by = 'published'
