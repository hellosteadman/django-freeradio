from django.conf import settings
from django.utils import six
from xml.etree import ElementTree as ET

import json
import logging
import re
import requests

if six.PY2:
    from urlparse import urlparse, urljoin
    from urllib import urlencode
else:
    from urllib.parse import urlparse, urljoin, urlencode

URL_REGEX = re.compile(
    r'<p>(?P<url>(?:http|ftp)s?://'
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)'
    r'+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
    r'localhost|'
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    r'(?::\d+)?'
    r'(?:/?|[/?]\S+))\s*<\/p>', re.IGNORECASE
)

URL_PATTERNS = getattr(settings, 'OEMBED_URLPATTERNS', ()) + (
    (
        'http://www.23hq.com/*/photo/*',
        'http://www.23hq.com/23/oembed',
        'xml'
    ),
    (
        (
            'https://alpha.app.net/*/post/*',
            'https://photos.app.net/*/*'
        ),
        'https://alpha-api.app.net/oembed',
        'json'
    ),
    (
        'http://live.amcharts.com/*',
        'http://live.amcharts.com/oembed',
        'json'
    ),
    (
        (
            'https://www.animatron.com/project/*',
            'https://animatron.com/project/*'
        ),
        'https://animatron.com/oembed/json',
        'json'
    ),
    (
        'http://animoto.com/play/*',
        'http://animoto.com/oembeds/create',
        'xml'
    ),
    (
        (
            'https://blackfire.io/profiles/*/graph',
            'https://blackfire.io/profiles/compare/*/graph'
        ),
        'https://blackfire.io/oembed',
        'json'
    ),
    (
        'http://movies.boxofficebuz.com/video/*',
        'http://boxofficebuz.com/oembed',
        'json'
    ),
    (
        'https://cacoo.com/diagrams/*',
        'http://cacoo.com/oembed.json',
        'json'
    ),
    (
        'http://img.catbo.at/*',
        'http://img.catbo.at/oembed.json',
        'json'
    ),
    (
        'http://public.chartblocks.com/c/*',
        'http://embed.chartblocks.com/1.0/oembed',
        'json'
    ),
    (
        'http://chirb.it/*',
        'http://chirb.it/oembed.json',
        'json'
    ),
    (
        'https://www.circuitlab.com/circuit/*',
        'https://www.circuitlab.com/circuit/oembed/',
        'json'
    ),
    (
        (
            'http://www.clipland.com/v/*',
            'https://www.clipland.com/v/*'
        ),
        'https://www.clipland.com/api/oembed',
        'json'
    ),
    (
        (
            'http://clyp.it/*',
            'http://clyp.it/playlist/*'
        ),
        'http://api.clyp.it/oembed/',
        'json'
    ),
    (
        (
            'http://codepen.io/*',
            'https://codepen.io/*'
        ),
        'http://codepen.io/api/oembed',
        'json'
    ),
    (
        (
            'http://codepoints.net/*',
            'https://codepoints.net/*',
            'http://www.codepoints.net/*',
            'https://www.codepoints.net/*'
        ),
        'https://codepoints.net/api/v1/oembed',
        'json'
    ),
    (
        'http://www.collegehumor.com/video/*',
        'http://www.collegehumor.com/oembed.json',
        'json'
    ),
    (
        (
            'http://coub.com/view/*',
            'http://coub.com/embed/*'
        ),
        'http://coub.com/api/oembed.json',
        'json'
    ),
    (
        'http://crowdranking.com/*/*',
        'http://crowdranking.com/api/oembed.json',
        'json'
    ),
    (
        'http://www.dailymile.com/people/*/entries/*',
        'http://api.dailymile.com/oembed',
        'json'
    ),
    (
        'http://www.dailymotion.com/video/*',
        'http://www.dailymotion.com/services/oembed',
        'json'
    ),
    (
        (
            'http://*.deviantart.com/art/*',
            'http://*.deviantart.com/*#/d*',
            'http://fav.me/*',
            'http://sta.sh/*'
        ),
        'http://backend.deviantart.com/oembed',
        'xml'
    ),
    (
        'https://*.didacte.com/a/course/*',
        'https://*.didacte.com/cards/oembed',
        'json'
    ),
    (
        'http://www.dipity.com/*/*/',
        'http://www.dipity.com/oembed/timeline/',
        'xml'
    ),
    (
        (
            'https://docs.com/*',
            'https://www.docs.com/*'
        ),
        'https://docs.com/api/oembed',
        'json'
    ),
    (
        'http://dotsub.com/view/*',
        'http://dotsub.com/services/oembed',
        'xml'
    ),
    (
        'http://edocr.com/docs/*',
        'http://edocr.com/api/oembed',
        'json'
    ),
    (
        'https://www.edumedia-sciences.com/*/media/*',
        'https://www.edumedia-sciences.com/oembed.json',
        'json'
    ),
    (
        'http://egliseinfo.catholique.fr/*',
        'http://egliseinfo.catholique.fr/api/oembed',
        'json'
    ),
    (
        (
            'https://www.facebook.com/*/videos/*',
            'https://www.facebook.com/video.php'
        ),
        'https://www.facebook.com/plugins/video/oembed.json',
        'json'
    ),
    (
        (
            'http://*.flickr.com/photos/*',
            'https://*.flickr.com/photos/*',
            'http://flic.kr/p/*',
            'https://flic.kr/p/*'
        ),
        'http://www.flickr.com/services/oembed/',
        'xml'
    ),
    (
        'http://www.funnyordie.com/videos/*',
        'http://www.funnyordie.com/oembed.json',
        'json'
    ),
    (
        (
            'http://*.geograph.org.uk/*',
            'http://*.geograph.co.uk/*',
            'http://*.geograph.ie/*',
            'http://*.wikimedia.org/*_geograph.org.uk_*'
        ),
        'http://api.geograph.org.uk/api/oembed',
        'json'
    ),
    (
        (
            'http://*.geograph.org.gg/*',
            'http://*.geograph.org.je/*',
            'http://channel-islands.geograph.org/*',
            'http://channel-islands.geographs.org/*',
            'http://*.channel.geographs.org/*'
        ),
        'http://www.geograph.org.gg/api/oembed',
        'xml'
    ),
    (
        (
            'http://geo-en.hlipp.de/*',
            'http://geo.hlipp.de/*',
            'http://germany.geograph.org/*'
        ),
        'http://geo.hlipp.de/restapi.php/api/oembed',
        'json'
    ),
    (
        'http://gty.im/*',
        'http://embed.gettyimages.com/oembed',
        'json'
    ),
    (
        (
            'http://gfycat.com/*',
            'http://www.gfycat.com/*',
            'https://gfycat.com/*',
            'https://www.gfycat.com/*'
        ),
        'https://api.gfycat.com/v1/oembed',
        'json'
    ),
    (
        'https://gyazo.com/*',
        'https://api.gyazo.com/api/oembed',
        'json'
    ),
    (
        'http://huffduffer.com/*/*',
        'http://huffduffer.com/oembed',
        'xml'
    ),
    (
        'http://www.hulu.com/watch/*',
        'http://www.hulu.com/api/oembed.json',
        'json'
    ),
    (
        'http://www.ifixit.com/Guide/View/*',
        'http://www.ifixit.com/Embed',
        'json'
    ),
    (
        'http://ifttt.com/recipes/*',
        'http://www.ifttt.com/oembed/',
        'json'
    ),
    (
        'https://player.indacolive.com/player/jwp/clients/*',
        'https://player.indacolive.com/services/oembed',
        'json'
    ),
    (
        'https://infogr.am/*',
        'https://infogr.am/oembed',
        'json'
    ),
    (
        (
            'http://instagram.com/p/*',
            'http://www.instagram.com/p/*',
            'http://instagr.am/p/*',
            'http://www.instagr.am/p/*',
            'https://instagram.com/p/*',
            'https://www.instagram.com/p/*',
            'https://instagr.am/p/*',
            'https://www.instagr.am/p/*'
        ),
        'http://api.instagram.com/oembed',
        'json'
    ),
    (
        (
            'http://www.kickstarter.com/projects/*',
            'https://www.kickstarter.com/projects/*'
        ),
        'http://www.kickstarter.com/services/oembed',
        'json'
    ),
    (
        (
            'https://www.kidoju.com/en/x/*/*',
            'https://www.kidoju.com/fr/x/*/*'
        ),
        'https://www.kidoju.com/api/oembed',
        'json'
    ),
    (
        'http://learningapps.org/*',
        'http://learningapps.org/oembed.php',
        'json'
    ),
    (
        'http://mathembed.com/latex?inputText=*',
        'http://mathembed.com/oembed',
        'json'
    ),
    (
        (
            'http://meetup.com/*',
            'http://meetu.ps/*'
        ),
        'https://api.meetup.com/oembed',
        'json'
    ),
    (
        'http://www.mixcloud.com/*/*/',
        'http://www.mixcloud.com/oembed/',
        'xml'
    ),
    (
        (
            'http://www.mobypicture.com/user/*/view/*',
            'http://moby.to/*'
        ),
        'http://api.mobypicture.com/oEmbed',
        'xml'
    ),
    (
        'https://beta.modelo.io/embedded/*',
        'https://portal.modelo.io/oembed',
        'json'
    ),
    (
        'https://mybeweeg.com/w/*',
        'https://mybeweeg.com/services/oembed',
        'json'
    ),
    (
        'http://*.nfb.ca/film/*',
        'http://www.nfb.ca/remote/services/oembed/',
        'xml'
    ),
    (
        (
            'https://mix.office.com/watch/*',
            'https://mix.office.com/embed/*'
        ),
        'https://mix.office.com/oembed',
        'json'
    ),
    (
        (
            'http://official.fm/tracks/*',
            'http://official.fm/playlists/*'
        ),
        'http://official.fm/services/oembed.json',
        'json'
    ),
    (
        'https://www.oumy.com/v/*',
        'https://www.oumy.com/oembed',
        'json'
    ),
    (
        (
            'http://pastery.net/*',
            'https://pastery.net/*',
            'http://www.pastery.net/*',
            'https://www.pastery.net/*'
        ),
        'https://www.pastery.net/oembed',
        'json'
    ),
    (
        (
            'http://*.polldaddy.com/s/*',
            'http://*.polldaddy.com/poll/*',
            'http://*.polldaddy.com/ratings/*'
        ),
        'http://polldaddy.com/oembed/',
        'xml'
    ),
    (
        'https://portfolium.com/entry/*',
        'https://api.portfolium.com/oembed',
        'json'
    ),
    (
        'http://www.quiz.biz/quizz-*.html',
        'http://www.quiz.biz/api/oembed',
        'json'
    ),
    (
        'http://www.quizz.biz/quizz-*.html',
        'http://www.quizz.biz/api/oembed',
        'json'
    ),
    (
        'https://rapidengage.com/s/*',
        'https://rapidengage.com/api/oembed',
        'json'
    ),
    (
        'https://reddit.com/r/*/comments/*/*',
        'https://www.reddit.com/oembed',
        'json'
    ),
    (
        'http://rwire.com/*',
        'http://publisher.releasewire.com/oembed/',
        'json'
    ),
    (
        'http://repubhub.icopyright.net/freePost.act?*',
        'http://repubhub.icopyright.net/oembed.act',
        'json'
    ),
    (
        (
            'https://www.reverbnation.com/*',
            'https://www.reverbnation.com/*/songs/*'
        ),
        'https://www.reverbnation.com/oembed',
        'xml'
    ),
    (
        (
            'http://roomshare.jp/post/*',
            'http://roomshare.jp/en/post/*'
        ),
        'http://roomshare.jp/en/oembed.json',
        'json'
    ),
    (
        'https://rumble.com/*.html',
        'https://rumble.com/api/Media/oembed.json',
        'json'
    ),
    (
        'http://videos.sapo.pt/*',
        'http://videos.sapo.pt/oembed',
        'xml'
    ),
    (
        'http://www.screenr.com/*/',
        'http://www.screenr.com/api/oembed.json',
        'json'
    ),
    (
        'http://www.scribd.com/doc/*',
        'http://www.scribd.com/services/oembed/',
        'xml'
    ),
    (
        'https://www.shortnote.jp/view/notes/*',
        'https://www.shortnote.jp/oembed/',
        'json'
    ),
    (
        (
            'http://shoudio.com/*',
            'http://shoud.io/*'
        ),
        'http://shoudio.com/api/oembed',
        'xml'
    ),
    (
        'https://showtheway.io/to/*',
        'https://showtheway.io/oembed',
        'json'
    ),
    (
        'https://onsizzle.com/i/*',
        'https://onsizzle.com/oembed',
        'json'
    ),
    (
        (
            'http://sketchfab.com/models/*',
            'https://sketchfab.com/models/*',
            'https://sketchfab.com/*/folders/*'
        ),
        'http://sketchfab.com/oembed',
        'json'
    ),
    (
        (
            'http://www.slideshare.net/*/*',
            'http://fr.slideshare.net/*/*',
            'http://de.slideshare.net/*/*',
            'http://es.slideshare.net/*/*',
            'http://pt.slideshare.net/*/*'
        ),
        'http://www.slideshare.net/api/oembed/2',
        'json'
    ),
    (
        (
            'http://soundcloud.com/*',
            'http://www.soundcloud.com/*',
            'https://soundcloud.com/*',
            'https://www.soundcloud.com/*'
        ),
        'https://soundcloud.com/oembed?format=json',
        'json'
    ),
    (
        (
            'https://play.soundsgood.co/playlist/*',
            'https://soundsgood.co/playlist/*'
        ),
        'https://play.soundsgood.co/oembed',
        'json'
    ),
    (
        (
            'http://speakerdeck.com/*/*',
            'https://speakerdeck.com/*/*'
        ),
        'https://speakerdeck.com/oembed.json',
        'json'
    ),
    (
        (
            'http://*.spreaker.com/*',
            'https://*.spreaker.com/*'
        ),
        'https://api.spreaker.com/oembed',
        'json'
    ),
    (
        (
            'http://streamable.com/*',
            'https://streamable.com/*'
        ),
        'https://api.streamable.com/oembed.json',
        'json'
    ),
    (
        'https://content.streamonecloud.net/embed/*',
        'https://content.streamonecloud.net/oembed',
        'json'
    ),
    (
        (
            'https://sway.com/*',
            'https://www.sway.com/*'
        ),
        'https://sway.com/api/v1.0/oembed',
        'json'
    ),
    (
        'http://ted.com/talks/*',
        'http://www.ted.com/talks/oembed.json',
        'json'
    ),
    (
        'https://www.nytimes.com/svc/oembed',
        'https://www.nytimes.com/svc/oembed',
        'json'
    ),
    (
        'https://theysaidso.com/image/*',
        'https://theysaidso.com/extensions/oembed/',
        'json'
    ),
    (
        (
            'http://clips.twitch.tv/*',
            'https://clips.twitch.tv/*',
            'http://www.twitch.tv/*',
            'https://www.twitch.tv/*',
            'http://twitch.tv/*',
            'https://twitch.tv/*'
        ),
        'https//api.twitch.tv/v4/oembed',
        'json'
    ),
    (
        (
            'http://*.ustream.tv/*',
            'http://*.ustream.com/*'
        ),
        'http://www.ustream.tv/oembed',
        'json'
    ),
    (
        'http://uttles.com/uttle/*',
        'http://uttles.com/api/reply/oembed',
        'json'
    ),
    (
        'http://verse.media/embed/#/stories/*',
        'http://verse.media/services/oembed/',
        'json'
    ),
    (
        (
            'http://www.videojug.com/film/*',
            'http://www.videojug.com/interview/*'
        ),
        'http://www.videojug.com/oembed.json',
        'json'
    ),
    (
        'https://vidl.it/*',
        'https://api.vidl.it/oembed',
        'json'
    ),
    (
        (
            'https://vimeo.com/*',
            'https://vimeo.com/album/*/video/*',
            'https://vimeo.com/channels/*/*',
            'https://vimeo.com/groups/*/videos/*',
            'https://vimeo.com/ondemand/*/*',
            'https://player.vimeo.com/video/*'
        ),
        'https://vimeo.com/api/oembed.json',
        'json'
    ),
    (
        (
            'http://vine.co/v/*',
            'https://vine.co/v/*'
        ),
        'https://vine.co/oembed.json',
        'json'
    ),
    (
        'https://*.wiredrive.com/*',
        'http://*.wiredrive.com/present-oembed/',
        'json'
    ),
    (
        (
            'http://*.wizer.me/learn/*',
            'https://*.wizer.me/learn/*',
            'http://*.wizer.me/preview/*',
            'https://*.wizer.me/preview/*'
        ),
        'http://app.wizer.me/api/oembed.json',
        'json'
    ),
    (
        'http://www.wootled.com/*/*',
        'http://www.wootled.com/oembed',
        'json'
    ),
    (
        (
            'http://*.yfrog.com/*',
            'http://yfrog.us/*'
        ),
        'http://www.yfrog.com/api/oembed',
        'json'
    ),
    (
        (
            'http://www.youtube.com/watch?v=*',
            'https://www.youtube.com/watch?v=*',
            'http://youtu.be/*',
            'https://youtu.be/*'
        ),
        'http://www.youtube.com/oembed',
        'json'
    )
)


LINK_REGEX = re.compile(r'\<link[^\>]+\>', re.IGNORECASE)
ATTR_REGEX = re.compile(
    r""" ([a-z]+)=(?:"([^"]+)"|'([^']+)')""",
    re.IGNORECASE
)

LINK_TYPE_REGEX = re.compile(r'^application/(json|xml)\+oembed$')

OEMBED_LOGGER = logging.getLogger('oembed')


def get_oembed_endpoint(url):
    for (patterns, endpoint, fmt) in URL_PATTERNS:
        if not isinstance(patterns, (list, tuple)):
            patterns = [patterns]

        for pattern in [
            re.compile(
                p.replace(
                    '*', '.*'
                ).replace(
                    '.', '\\.'
                ).replace(
                    '?', '\\?'
                ),
                re.IGNORECASE
            ) for p in patterns
        ]:
            if pattern.match(url) is not None:
                return endpoint, fmt

    return None, None


def get_oembed_response(url, endpoint, fmt, width=None):
    if not width:
        width = getattr(settings, 'OEMBED_WIDTH', 640)

    if fmt == 'json':
        mimetype = 'application/json'
    elif fmt == 'xml':
        mimetype = 'text/xml'
    elif fmt != 'html':
        raise Exception(
            'Handler configured incorrectly (unrecognised format %s)' % fmt
        )

    params = {
        'url': url
    }

    if int(width) > 0:
        params['width'] = width
        params['maxwidth'] = width

    if not callable(endpoint):
        oembed_response = requests.get(
            endpoint,
            params=params,
            headers={
                'Accept': mimetype,
                'User-Agent': 'django'
            }
        )

        if oembed_response.status_code >= 200:
            if oembed_response.status_code < 400:
                return oembed_response.content

        oembed_response.raise_for_status()

    return endpoint(url, width)


def parse_oembed_response(response, fmt):
    if fmt == 'html':
        return response

    if fmt == 'json':
        data = json.loads(response)

        if 'html' in data:
            return data.get('html')

        if 'thumbnail_url' in data:
            return (
                u'<a href="%(resource)s">'
                u'<img alt=="%(title)s" src="%(url)s" />'
                u'</a>'
            ) % {
                'title': data['title'],
                'url': data['thumbnail_url'],
                'resource': url,
            }

        raise Exception('Response not understood', data)

    xml = ET.fromstring(response)
    return xml.find('html').text or ''


def get_oembed_content(url, endpoint, fmt, width=None):
    response = get_oembed_response(url, endpoint, fmt, width)
    return parse_oembed_response(response, fmt)


def guess_oembed_content(url, width):
    html = requests.get(url).content
    matches = LINK_REGEX.findall(html)

    for match in matches:
        attrs = {}
        for attr in ATTR_REGEX.findall(match):
            key, value1, value2 = attr
            attrs[key] = value1 or value2

        if attrs.get('rel') == 'alternate':
            fmt = LINK_TYPE_REGEX.match(attrs.get('type', ''))
            if fmt is not None:
                fmt = fmt.groups()[0]
                url = attrs.get('href')
                urlparts = urlparse(url)
                params = parse_qs(urlparts.query or urlparts.params)
                q = url.find('?')

                if q > -1:
                    url = url[:q]

                params['width'] = width
                params['maxwidth'] = width

                oembed_response = requests.get(
                    url,
                    params=params,
                    headers={
                        'Accept': {
                            'json': 'application/json',
                            'xml': 'text/aml'
                        }[fmt],
                        'User-Agent': 'django'
                    }
                )

                if oembed_response.status_code >= 200:
                    if oembed_response.status_code < 400:
                        return parse_oembed_response(
                            oembed_response.content,
                            fmt
                        )


def sandbox_iframe(html):
    if html:
        return html.replace(
            '<iframe ',
            '<iframe sandbox="allow-pointer-lock allow-scripts" '
        )

    return html
