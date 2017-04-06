from datetime import timedelta
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.text import slugify, mark_safe
from hashlib import md5
from .helpers import upload_presenter_photo, calculate_next_air_dates
from .managers import ProgrammeManager


class Series(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(max_length=30, unique=True)
    subtitle = models.CharField(max_length=200, null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('slug',)


class Programme(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(max_length=30, unique=True)
    subtitle = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    series = models.ForeignKey(
        Series,
        related_name='programmes',
        null=True,
        blank=True
    )

    presenters = models.ManyToManyField(
        'talent.Presenter',
        through='ProgrammePresenter'
    )

    mon_start = models.CharField(max_length=5, null=True, blank=True)
    mon_end = models.CharField(max_length=5, null=True, blank=True)
    tue_start = models.CharField(max_length=5, null=True, blank=True)
    tue_end = models.CharField(max_length=5, null=True, blank=True)
    wed_start = models.CharField(max_length=5, null=True, blank=True)
    wed_end = models.CharField(max_length=5, null=True, blank=True)
    thu_start = models.CharField(max_length=5, null=True, blank=True)
    thu_end = models.CharField(max_length=5, null=True, blank=True)
    fri_start = models.CharField(max_length=5, null=True, blank=True)
    fri_end = models.CharField(max_length=5, null=True, blank=True)
    sat_start = models.CharField(max_length=5, null=True, blank=True)
    sat_end = models.CharField(max_length=5, null=True, blank=True)
    sun_start = models.CharField(max_length=5, null=True, blank=True)
    sun_end = models.CharField(max_length=5, null=True, blank=True)

    recurrence = models.IntegerField(
        choices=(
            (7, u'every week'),
            (14, u'every 2 weeks'),
            (-2, u'every month'),
            (-1, u'one-off')
        ),
        default=7
    )

    monthly_number = models.PositiveIntegerField(
        choices=(
            (1, u'1st'),
            (2, u'2nd'),
            (3, u'3rd'),
            (4, u'4th'),
            (6, u'last')
        ),
        null=True, blank=True
    )

    monthly_weekday = models.PositiveIntegerField(
        choices={
            (0, 'Monday'),
            (1, 'Tuesday'),
            (2, 'Wednesday'),
            (3, 'Thursday'),
            (4, 'Friday'),
            (5, 'Saturday'),
            (6, 'Sunday')
        },
        null=True, blank=True
    )

    next_air_date = models.DateField(
        help_text=(
            u'Used to determine what to use as a base date for shows '
            u'that are not weekly'
        ),
        null=True, blank=True
    )

    archived = models.BooleanField(default=False)
    banner = models.ImageField(
        upload_to='upload_programme_banner',
        max_length=255,
        null=True,
        blank=True
    )

    logo = models.ImageField(
        upload_to='upload_programme_logo',
        max_length=255,
        null=True,
        blank=True
    )

    objects = ProgrammeManager()

    def __unicode__(self):
        return self.name or self.get_presenters_display()

    @models.permalink
    def get_absolute_url(self):
        return ('traffic:programme', [self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(self))

        rightnow = timezone.localtime(
            timezone.now()
        ).date()

        if (
            self.next_air_date is None
        ) or (
            (rightnow - self.next_air_date).days > 1
        ):
            next_air_date = self.calculate_next_air_date()
            self.next_air_date = (
                next_air_date and
                next_air_date.date() or
                None
            )

        super(Programme, self).save(*args, **kwargs)

    def calculate_next_air_date(self):
        for date in calculate_next_air_dates(self):
            return date

    def get_tx_display(self):
        def f(value):
            time = value.split(':')
            hour, minute = [int(p) for p in time]

            if minute == 0:
                if hour > 12:
                    return '%dpm' % (hour - 12)

                if hour == 0:
                    return 'midnight'

                if hour < 12:
                    return '%dam' % hour

                return 'noon'

            if hour >= 12:
                return '%d:%spm' % (
                    hour - 12,
                    str(minute).zfill(2)
                )

            if hour == 0:
                return '12:%sam' % (
                    str(minute).zfill(2)
                )

            return '%d:%sam' % (
                hour,
                str(minute).zfill(2)
            )

        if self.recurrence == -1:
            if self.next_air_date is None:
                return

            weekday_name = {
                0: 'mon',
                1: 'tue',
                2: 'wed',
                3: 'thu',
                4: 'fri',
                5: 'sat',
                6: 'sun'
            }[self.next_air_date.weekday()]

            time = getattr(self, '%s_start' % weekday_name)
            return self.next_air_date.strftime(
                '%s from %s' % (
                    self.next_air_date.strftime('%A'),
                    f(time)
                )
            )

        if self.recurrence == -2:
            return 'Every %s %s, %s' % (
                {
                    1: 'first',
                    2: 'second',
                    3: 'third',
                    4: 'fourth',
                    5: 'first',
                    6: 'last'
                }[self.monthly_number],
                {
                    0: 'Monday',
                    1: 'Tuesday',
                    2: 'Wednesday',
                    3: 'Thursday',
                    4: 'Friday',
                    5: 'Saturday',
                    6: 'Sunday'
                }[self.monthly_weekday],
                f(
                    getattr(
                        self,
                        '%s_start' % {
                            0: 'mon',
                            1: 'tue',
                            2: 'wed',
                            3: 'thu',
                            4: 'fri',
                            5: 'sat',
                            6: 'sun'
                        }[self.monthly_weekday]
                    )
                )
            )

        def a(label, is_weekday):
            if self.recurrence == 14:
                return 'Alternate %s' % label, is_weekday
            else:
                return label, is_weekday

        days = {
            'mon': a('Mondays', True),
            'tue': a('Tuesdays', True),
            'wed': a('Wednesdays', True),
            'thu': a('Thursdays', True),
            'fri': a('Fridays', True),
            'sat': a('Saturdays', False),
            'sun': a('Sundays', False)
        }

        tx_days = {}
        day_groups = {
            'mon': None,
            'tue': None,
            'wed': None,
            'thu': None,
            'fri': None,
            'sat': None,
            'sun': None
        }

        for day, (label, weekday) in days.items():
            start = getattr(self, '%s_start' % day)
            if start:
                if day in ('mon', 'tue', 'wed', 'thu', 'fri'):
                    day_groups[day] = start

                elif day in ('sat', 'sun'):
                    day_groups[day] = start

        weekdays_hash = ' '.join(
            set(
                (
                    day_groups['mon'] or ' ',
                    day_groups['tue'] or ' ',
                    day_groups['wed'] or ' ',
                    day_groups['thu'] or ' ',
                    day_groups['fri'] or ' '
                )
            )
        )

        if len(weekdays_hash) == 5:
            day_groups['weekdays'] = weekdays_hash
            for day in ('mon', 'tue', 'wed', 'thu', 'fri'):
                del day_groups[day]

        weekends_hash = ' '.join(
            set(
                (
                    day_groups['sat'] or ' ',
                    day_groups['sun'] or ' '
                )
            )
        )

        if len(weekends_hash) == 5:
            day_groups['weekends'] = weekends_hash
            for day in ('sat', 'sun'):
                del day_groups[day]

        alldays_hash = ' '.join(
            set(
                (
                    day_groups.get('weekdays', ' '),
                    day_groups.get('weekends', ' ')
                )
            )
        )

        if len(alldays_hash) == 5:
            day_groups['daily'] = alldays_hash
            for day in ('weekdays', 'weekends'):
                del day_groups[day]

        tx_parts = []
        time_groups = {}

        for group in ('mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'):
            time = day_groups.get(group)
            if not time:
                continue

            if time not in time_groups:
                time_groups[time] = [group]
            else:
                time_groups[time].append(group)

        for time, group in time_groups.items():
            if len(group) == 1:
                continue

            for g in group:
                del day_groups[g]

            if len(group) == 2:
                group = '%s and %s' % (
                    days[group[0]][0],
                    days[group[1]][0]
                )
            elif len(group) > 2:
                group = '%s and %s' % (
                    ', '.join(
                        [
                            days[g][0]
                            for g in group[0:-1]
                        ]
                    ),
                    days[group[-1]][0]
                )

            day_groups[group] = time

        previous_time = None
        previous_group = None
        for group in (
            'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun',
            'weekdays', 'weekends', 'daily'
        ):
            time = day_groups.pop(group, None)
            if not time:
                if previous_time is not None:
                    previous_time = None
                    previous_group = None

                continue

            if group in ('weekdays', 'weekends', 'daily'):
                tx_parts.append(
                    '%s from %s' % (
                        group,
                        f(time)
                    )
                )
            else:
                if previous_time is not None:
                    if previous_time != time:
                        previous_time = time
                        previous_group = group
                    else:
                        tx_parts[-1] = '%s - %s from %s' % (
                            days[previous_group][0],
                            days[group][0],
                            f(time)
                        )

                        continue
                else:
                    previous_time = time
                    previous_group = group

                tx_parts.append(
                    '%s from %s' % (
                        days[group][0],
                        f(time)
                    )
                )

        for group, time in day_groups.items():
            tx_parts.insert(
                0,
                '%s from %s' % (
                    group,
                    f(time)
                )
            )

        return ', '.join(tx_parts)

    def get_presenters_display(self):
        presenter_names = list(
            self.programmepresenter_set.values_list(
                'presenter__name',
                flat=True
            )
        )

        if len(presenter_names) > 2:
            return '%s and %s' % (
                ', '.join(presenter_names[0:-1]),
                presenter_names[-1]
            )

        return ' and '.join(presenter_names)

    class Meta:
        ordering = ('name', 'slug')


class ProgrammePresenter(models.Model):
    programme = models.ForeignKey(Programme)
    presenter = models.ForeignKey(
        'talent.Presenter',
        related_name='programmes'
    )

    order = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return u'%s - %s' % (self.programme.name, self.presenter.name)

    class Meta:
        unique_together = ('presenter', 'programme')
        ordering = ('order',)
        db_table = 'traffic_programme_presenters'


class ProgrammeHiatus(models.Model):
    programme = models.ForeignKey(Programme, related_name='hiatuses')
    date = models.DateField()
    notes = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.date.strftime('%d/%m/%Y')

    class Meta:
        unique_together = ('date', 'programme')


class Update(models.Model):
    programme = models.ForeignKey(Programme, related_name='updates')
    date = models.DateTimeField()
    title = models.CharField(max_length=140, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    author = models.ForeignKey(
        'auth.User',
        related_name='programme_updates',
        null=True,
        blank=True
    )

    url = models.URLField(u'URL', max_length=255, null=True, blank=True)
    kind = models.CharField(
        max_length=10,
        choices=(
            ('info', u'Information'),
            ('warn', u'Warning'),
            ('danger', u'Danger'),
            ('success', u'Success'),
            ('episode', u'Episode'),
            ('post', u'Blog post')
        )
    )

    def __unicode__(self):
        return self.title or self.date.strftime('%Y-%m-%d')

    def render_media(self):
        cachekey = 'rendered_media_%s' % md5(self.url).hexdigest()
        rendered = cache.get(cachekey)

        if not rendered:
            rendered = (
                '<iframe width="100%%" height="60" '
                'src="https://www.mixcloud.com/widget/iframe/?feed=%s'
                '&hide_cover=1&mini=1&light=1" frameborder="0"></iframe>'
            ) % urlquote(self.url)

            cache.set(cachekey, rendered, 60 * 60 * 24)

        return mark_safe(rendered)

    class Meta:
        ordering = ('-date',)
        get_latest_by = 'date'


class MixcloudSearch(models.Model):
    programme = models.ForeignKey(
        'traffic.Programme',
        related_name='mixcloud_searches'
    )

    criteria = models.CharField(max_length=100)

    def __unicode__(self):
        return self.criteria

    class Meta:
        ordering = ('criteria',)
        unique_together = ('criteria', 'programme')


class Lookahead(models.Model):
    start = models.DateField()

    class Meta:
        ordering = ('-start',)


class LookaheadItem(models.Model):
    lookahead = models.ForeignKey(Lookahead, related_name='items')
    programme = models.ForeignKey(Programme, related_name='lookaheads')
    details = models.TextField()

    def __unicode__(self):
        return self.programme.name

    class Meta:
        unique_together = ('programme', 'lookahead')
