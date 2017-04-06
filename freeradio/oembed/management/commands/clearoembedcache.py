from django.core.management.base import BaseCommand
from ...models import Resource


class Command(BaseCommand):
    def handle(self, *args, **options):
        Resource.objects.all().delete()
