from django.template import Library
from django.contrib.auth.models import User
from django.utils.safestring import SafeText
from hashlib import md5
from sorl.thumbnail import get_thumbnail
from ..models import Blogger
from ...talent.models import Presenter

register = Library()


@register.filter
def avatar(user, size=150):
    if isinstance(user, (str, unicode, SafeText)) and '@' in user:
        return '//www.gravatar.com/avatar/%s?s=%s' % (
            md5(user).hexdigest(), size
        )

    if isinstance(user, User):
        try:
            if getattr(user, 'presenter_profile'):
                if user.presenter_profile.photo:
                    thumbnail = get_thumbnail(
                        user.presenter_profile.photo,
                        '%sx%s' % (size, size),
                        crop='center'
                    )

                    return thumbnail and thumbnail.url
        except Presenter.DoesNotExist:
            pass

        try:
            if getattr(user, 'blogger_profile'):
                if user.blogger_profile.photo:
                    thumbnail = get_thumbnail(
                        user.blogger_profile.photo,
                        '%sx%s' % (size, size),
                        crop='center'
                    )

                    return thumbnail and thumbnail.url
        except Blogger.DoesNotExist:
            pass

    if getattr(user, 'email', None):
        return '//www.gravatar.com/avatar/%s?s=%s' % (
            md5(user.email).hexdigest(), size
        )

    initials = ''.join(
        [
            n[0].upper()
            for n in (
                user.first_name and user.last_name
            ) and (
                user.get_full_name().split(' ')
            ) or [user.username]
        ]
    )

    return '//placehold.it/%sx%s?text=%s' % (
        size,
        size,
        initials
    )
