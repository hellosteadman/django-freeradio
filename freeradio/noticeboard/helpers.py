from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from .models import Notice


MODELS = getattr(settings, 'NOTICEBOARD_MODELS', ())


def add_or_update_notice(obj, **kwargs):
    content_type = ContentType.objects.get_for_model(obj)
    object_id = obj.pk
    options = {}

    for (model, attrs) in MODELS:
        app_label, model = model.split('.')
        if content_type.app_label == app_label:
            if content_type.model.lower() == model.lower():
                subtitle = attrs.get('subtitle', None)
                title = attrs.get('title', None)
                description = attrs.get('description', None)
                date = attrs.get('date', None)
                subtitle_field = attrs.get('subtitle_field', None)
                title_field = attrs.get('title_field', None)
                description_field = attrs.get('description_field', None)
                date_field = attrs.get('date_field', None)

                if subtitle:
                    if callable(subtitle):
                        options['subtitle'] = subtitle(obj)
                    else:
                        options['subtitle'] = subtitle
                elif subtitle_field:
                    options['subtitle'] = getattr(obj, subtitle_field)
                    if callable(options['subtitle']):
                        options['subtitle'] = options['subtitle'](obj)

                if title:
                    if callable(title):
                        options['title'] = title(obj)
                    else:
                        options['title'] = title
                elif title_field:
                    options['title'] = getattr(obj, title_field)
                    if callable(options['title']):
                        options['title'] = options['title'](obj)

                if description:
                    if callable(description):
                        options['description'] = description(obj)
                    else:
                        options['description'] = description
                elif description_field:
                    options['description'] = getattr(
                        obj, description_field
                    )

                    if callable(options['description']):
                        options['description'] = options['description'](
                            obj
                        )

                if 'image_field' in attrs:
                    options['image_field'] = attrs['image_field']

                if 'stickiness' in attrs:
                    options['stickiness'] = attrs['stickiness']

                if 'cta_text' in attrs:
                    options['cta_text'] = attrs['cta_text']
                    if callable(options['cta_text']):
                        options['cta_text'] = options['cta_text'](obj)

                if 'cta_url' in attrs:
                    options['cta_url'] = attrs['cta_url']
                    if callable(options['cta_url']):
                        options['cta_url'] = options['cta_url'](obj)

                if date:
                    if callable(date):
                        options['date'] = date(obj)
                    else:
                        options['date'] = date
                elif date_field:
                    options['date'] = getattr(obj, date_field)
                    if callable(options['date']):
                        options['date'] = options['date'](obj)

                break

    options.update(kwargs)
    subtitle = options.pop('subtitle', subtitle) or str(
        obj._meta.verbose_name
    )

    title = options.pop('title', title) or str(obj)
    description = options.pop('description', None)
    image_field = options.pop('image_field', None)
    stickiness = options.pop('stickiness', 0)
    cta_text = options.pop('cta_text', None)
    cta_url = options.pop('cta_url', None) or obj.get_absolute_url()
    added = options.pop('date', None) or timezone.localtime(timezone.now())

    if Notice.objects.filter(
        content_type=content_type,
        object_id=object_id
    ).exists():
        Notice.objects.filter(
            content_type=content_type,
            object_id=object_id
        ).update(
            subtitle=subtitle,
            title=title,
            description=description,
            image_field=image_field,
            cta_text=cta_text,
            cta_url=cta_url,
            stickiness=stickiness,
            added=added
        )
    else:
        Notice.objects.create(
            content_type=content_type,
            object_id=object_id,
            subtitle=subtitle,
            title=title,
            description=description,
            image_field=image_field,
            stickiness=stickiness,
            cta_text=cta_text,
            cta_url=cta_url,
            added=added
        )


def fill_area(notices, area_size, start_from=0):
    area_to_cover = area_size
    skipped = []

    for notice in notices[start_from:start_from + 32]:
        width, height = notice.get_blocks()
        block_area = width * height
        remaining_area = area_to_cover - block_area

        if remaining_area >= 0:
            yield notice
            area_to_cover -= block_area
        else:
            break
