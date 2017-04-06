from collections import OrderedDict
from django.contrib.auth.models import User
from django.core.files import File
from django.core.management.base import BaseCommand, CommandError
from django.utils.html import strip_tags
from django.utils.timezone import utc
from django.template.defaultfilters import slugify
from html2text import html2text
from markdown2 import markdown
from os import sys, write, close, remove, path
from tempfile import mkstemp
from django.utils import six
from ....blog.models import Post, Category as Category
from ....traffic.models import Programme
from ....talent.models import Presenter
import phpserialize
import re
import requests
import wp_export_parser

if six.PY2:
    from urlparse import urlparse, urljoin
else:
    from urllib.parse import urlparse, urljoin


def get_categories(post):
    categories = post.findall('category')
    d = {}

    for c in categories:
        o = c.get('domain')
        if o in d:
            d[o].append(c.text)
        else:
            d[o] = [c.text]

    return d


def parse_post(post):
    out = {
        'postmeta': {}
    }

    for element in post.getiterator():
        if 'title' in element.tag:
            out['title'] = element.text
        elif 'post_name' in element.tag:
            out['post_name'] = element.text
        elif 'post_id' in element.tag:
            out['post_id'] = element.text
        elif 'post_type' in element.tag:
            out['post_type'] = element.text
        elif 'pubDate' in element.tag and element.text:
            out['pubDate'] = wp_export_parser.parse.parse_pubdate(
                element.text
            )
        elif 'status' in element.tag:
            out['status'] = element.text
        elif 'link' in element.tag:
            out['link'] = element.text
        elif 'encoded' in element.tag and 'content' in element.tag:
            out['body'] = wp_export_parser.parse_shortcodes.parse(
                wp_export_parser.autop.wpautop(element.text)
            )

        elif 'postmeta' in element.tag:
            for meta_element in element.getchildren():
                if 'meta_key' in meta_element.tag:
                    key = meta_element.text
                elif 'meta_value' in meta_element.tag:
                    value = meta_element.text

            out['postmeta'][key] = value
        elif 'creator' in element.tag:
            out['creator'] = element.text

    return out


wp_export_parser.parse.get_categories = get_categories
wp_export_parser.parse.parse_post = parse_post


def try_to_unserialise(value):
    try:
        return phpserialize.loads(value)
    except Exception, ex:
        print value
        print
        raise CommandError(str(ex))


class Command(BaseCommand):
    def download(self, u):
        response = requests.get(u, stream=True)
        ext = path.splitext(urlparse(u).path)[-1]
        handle, filename = mkstemp(ext)

        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                write(handle, chunk)

        close(handle)
        return File(
            open(filename, 'r'),
            name=path.split(urlparse(u).path)[-1]
        )

    def match_attachment(self, post, parent):
        post_id = int(post.get('post_id'))
        return int(getattr(parent, '_thumbnail_id', 0)) == post_id

    def attach_image(self, post, parent, domain):
        meta = post.pop('postmeta', {})
        title = post.pop('title', u'')

        am = meta.pop('_wp_attachment_metadata', None)
        if not am:
            return

        for url in re.findall(r'"file";s:\d+:"([^"]+)"', am):
            url = urljoin(
                'http://%s/wp-content/uploads/' % domain,
                url
            )

            if parent.featured_image and parent.featured_image.name == (
                'blog/%s' % path.split(urlparse(url).path)[-1]
            ):
                return

            parent.featured_image = self.download(url)
            parent.save(update_fields=('featured_image',))
            self.stdout.write('Downloaded image for %s\n' % str(parent))
            return

    def import_author(self, username):
        try:
            return User.objects.get(
                username__iexact=username
            )
        except User.DoesNotExist:
            user = User(username=username.lower())
            user.set_password('temp1234')
            user.is_staff = True
            user.save()
            return user

    def import_post(self, item, category_name):
        title = item.pop('title')
        body = item.pop('body')
        slug = item.pop('post_name')[:30]
        date = item.pop('pubDate').replace(tzinfo=utc)

        try:
            category = Category.objects.get(
                name=category_name
            )
        except Category.DoesNotExist:
            category = Category.objects.create(
                name=category_name,
                slug=slugify(category_name)
            )

        body = body.strip()
        if not body:
            return

        body = html2text(body, bodywidth=10000)
        if not body:
            return

        if title.upper() == title:
            title = title.title()

        kwargs = {
            'title': title,
            'published': date,
            'body': body
        }

        post_id = int(item.pop('post_id'))
        meta = item.pop('postmeta', {})

        for programme in Programme.objects.all():
            if programme.name and programme.name.lower() in title.lower():
                kwargs['date'] = kwargs.pop('published')
                kwargs['description'] = kwargs.pop('body')
                kwargs['kind'] = 'post'

                if title.lower().startswith(programme.name.lower()):
                    kwargs['title'] = (
                        title[len(programme.name) + 1:].capitalize()
                    )

                if not programme.updates.filter(
                    date=kwargs['date'],
                    kind='post'
                ).exists():
                    self.stdout.write('Created %s\n' % title)
                    return programme.updates.create(**kwargs)
                else:
                    self.stdout.write('Updated %s\n' % title)
                    progarmme.updates.filter(
                        date=kwargs['date'],
                        kind='post'
                    ).update(**kwargs)

        kwargs['body'] = markdown(kwargs['body'])
        kwargs['slug'] = slug
        kwargs['author'] = self.import_author(item.pop('creator'))

        try:
            po = Post.objects.get(slug=slug, published=date)
        except Post.DoesNotExist:
            c = Post.objects.filter(slug__startswith=slug).count()
            s = slug

            while Post.objects.filter(slug=s).exists():
                s = '%s-%d' % (
                    slug[:30-len('-%d' % c)],
                    c
                )

                c += 1

            kwargs['slug'] = s
            po = Post.objects.create(**kwargs)
            self.stdout.write('Created %s\n' % po.title)
        else:
            po.__dict__.update(kwargs)
            po.save()
            self.stdout.write('Updated %s\n' % po.title)

        po.categories.add(category)

        if '_thumbnail_id' in meta:
            thumbnail_id = int(meta.pop('_thumbnail_id'))
            po._thumbnail_id = thumbnail_id

        return po

    def handle(self, *args, **options):
        parser = wp_export_parser.WPParser(sys.stdin)
        domain = parser.get_domain()
        parents = []

        for post in parser.get_items():
            if post.pop('status') != 'publish':
                continue

            post_type = post.pop('post_type')
            if post_type == 'post':
                post = self.import_post(post, 'Reviews')
                if post is not None:
                    parents.append(post)

        for post in parser.get_items():
            if post.pop('post_type') == 'attachment':
                for parent in parents:
                    if self.match_attachment(post, parent):
                        self.attach_image(post, parent, domain)
