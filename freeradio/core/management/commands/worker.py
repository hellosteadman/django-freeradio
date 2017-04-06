from django.core.management.base import BaseCommand
from rq import Worker, Queue, Connection
import os
import redis


class Command(BaseCommand):
    def handle(self, *args, **options):
        listen = ['high', 'default', 'low']
        redis_url = os.getenv('REDIS_URL', 'redis://127.0.0.1:6379')
        conn = redis.from_url(redis_url)

        with Connection(conn):
            worker = Worker(map(Queue, listen))
            worker.work()
