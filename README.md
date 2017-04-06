Django Free Radio
=================

![Travis CI](https://travis-ci.org/iamsteadman/django-freeradio.svg?branch=master)

A Django project for managing a radio station for a community radio station.

The code was originally based on the Django website for [Brum Radio](https://brumradio.com/), and was open sourced as part of a sprint
session at [DjangoCon Europe 2017](http://2017.djangocon.eu/).

Try it via Heroku
-----------------

You can run the project via Heroku right now. By default it'll use free dynos,
but you will need an AWS access key and secret, and to create an S3 bucket, to
store static files and user-uploaded media

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/iamsteadman/django-freeradio)

Setup locally
-------------

Settings are managed using `django-environ`. Create your `.env` file based on
the proposed `env.example` file. Most importantly, set the following variables.
For example:

    DJANGO_SECRET_KEY="your-secret-key"
    DJANGO_DEBUG=True
