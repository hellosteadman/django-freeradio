Django Free Radio
=================

![Travis CI](https://travis-ci.org/iamsteadman/django-freeradio.svg?branch=master)

A Django project for managing a radio station for a community radio station.

The code was originally based on the Django website for [Brum Radio](https://brumradio.com/), and was open sourced as part of a sprint session at [DjangoCon Europe 2017](http://2017.djangocon.eu/).

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/iamsteadman/django-freeradio)

Setup
=====

Settings are managed using `django-environ`. Create your `.env` file based on
the proposed `env.example` file. Most importantly, set the following variables for
local development:

    DATABASE_URL="postgres://freeradio:freeradio@localhost:5432/freeradio"
    DJANGO_SETTINGS_MODULE="config.settings.local"
    DJANGO_SECRET_KEY="your-secret-key"
    DJANGO_DEBUG=True