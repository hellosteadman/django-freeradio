from django.core.management.base import BaseCommand
from ...models import Series


class Command(BaseCommand):
    def handle(self, *args, **options):
        for series in Series.objects.all():
            series.check_for_episodes()
