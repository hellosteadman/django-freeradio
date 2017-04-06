from django.core.management.base import BaseCommand
from ...helpers import search_mixcloud_for_updates


class Command(BaseCommand):
    def handle(self, *args, **options):
        search_mixcloud_for_updates()
