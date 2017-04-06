from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from ...helpers import add_or_update_notice


class Command(BaseCommand):
    def handle(self, *args, **options):
        for (model, attrs) in getattr(settings, 'NOTICEBOARD_MODELS', ()):
            app_label, model = model.split('.')
            content_type = ContentType.objects.get(
                app_label__iexact=app_label,
                model__iexact=model
            )

            for obj in content_type.model_class().objects.all():
                add_or_update_notice(obj)
