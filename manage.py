#!/usr/bin/env python
import sys
import environ

env = environ.Env()
env.read_env('.env')

if __name__ == '__main__':
    env('DJANGO_SETTINGS_MODULE', default='freeradio.settings')

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
