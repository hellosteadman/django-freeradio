from constance import config
from datetime import datetime, timedelta
from dateutil.parser import parse as parse_date
from django.utils import timezone
from math import ceil
from os import path
import re
import requests
import calendar


def upload_presenter_photo(instance, filename):
    return 'presenters/%s%s' % (
        instance.slug,
        path.splitext(filename)[-1]
    )


def upload_programme_banner(instance, filename):
    return 'programmes/%s.banner%s' % (
        instance.slug,
        path.splitext(filename)[-1]
    )


def upload_programme_logo(instance, filename):
    return 'programmes/%s.logo%s' % (
        instance.slug,
        path.splitext(filename)[-1]
    )


def week_of_month(date):
    first_day = date.replace(day=1)
    adjusted_day = date.day + first_day.weekday()
    return int(ceil(adjusted_day / 7.0))


def first_day_of_week_in_month(date, weekday):
    first_day_of_month = date.replace(day=1)
    first_matching_weekday = first_day_of_month + timedelta(
        days=(
            (weekday - calendar.monthrange(date.year, date.month)[0]) + 7
        ) % 7
    )

    return first_matching_weekday


def last_day_of_week_in_month(date, weekday):
    year = date.year
    month = date.month + 1

    if month == 13:
        month = 1
        year += 1

    return first_day_of_week_in_month(
        date.replace(
            month=month,
            year=year
        ),
        weekday
    ) - timedelta(days=7)


def calculate_next_air_dates(
    instance, max=10, include_today=False, include_end_date=False
):
    weekday_names = {
        0: 'mon',
        1: 'tue',
        2: 'wed',
        3: 'thu',
        4: 'fri',
        5: 'sat',
        6: 'sun'
    }

    rightnow = timezone.localtime(
        timezone.now()
    )

    today = rightnow.date()
    prev_air_date = rightnow.replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0
    )

    hiatuses = instance.hiatuses.filter(
        date__gte=today
    ).values_list('date', flat=True)

    while prev_air_date.weekday():
        prev_air_date -= timedelta(days=1)

    yielded = 0
    if instance.recurrence == -1:
        i = 0
        while True:
            date = prev_air_date + timedelta(days=i)
            weekday = date.weekday()
            time = getattr(instance, '%s_start' % weekday_names[weekday])
            end = getattr(instance, '%s_end' % weekday_names[weekday])
            i += 1

            if time:
                hour, minute = [int(p) for p in time.split(':')]
                date = date.replace(
                    hour=hour,
                    minute=minute,
                    second=0,
                    microsecond=0
                )

                if date.date() in hiatuses:
                    continue

                if (
                    date >= rightnow
                ) or (
                    date.date() == today and
                    include_today
                ):
                    if instance.archived:
                        return

                    if include_end_date:
                        hour, minute = [int(p) for p in end.split(':')]
                        date_end = date.replace(
                            hour=hour,
                            minute=minute,
                            second=0,
                            microsecond=0
                        ) - timedelta(seconds=1)

                        if not hour or hour < date.hour:
                            date_end += timedelta(days=1)

                        yield (
                            date,
                            date_end
                        )
                    else:
                        yield date

                    yielded += 1
                    if yielded == max:
                        return

            if i == 365:
                break
    elif instance.recurrence == -2:
        next_to_check = prev_air_date
        while True:
            first_of_month = first_day_of_week_in_month(
                next_to_check,
                instance.monthly_weekday
            )

            if instance.monthly_number > 5:
                last_day_of_month = last_day_of_week_in_month(
                    first_of_month,
                    instance.monthly_weekday
                )

                weeks_between = int(ceil(float(last_day_of_month.day) / 7.0))
                next_proposed_date = first_of_month + timedelta(
                    days=7 * weeks_between
                )

                if next_proposed_date > last_day_of_month:
                    next_proposed_date -= timedelta(days=7)

                date = next_proposed_date
            else:
                date = first_of_month + timedelta(
                    days=7 * (instance.monthly_number - 1)
                )

            d = next_to_check.day
            m = next_to_check.month + 1
            y = next_to_check.year

            if m == 13:
                m = 1
                y += 1

            fwd, dim = calendar.monthrange(y, m)
            if d > dim:
                d -= dim
                m += 1

                if m == 13:
                    m = 1
                    y += 1

            next_to_check = next_to_check.replace(
                day=d,
                month=m,
                year=y
            )

            time = getattr(
                instance,
                '%s_start' % weekday_names[instance.monthly_weekday]
            )

            end = getattr(
                instance,
                '%s_end' % weekday_names[instance.monthly_weekday]
            )

            if time:
                hour, minute = [int(p) for p in time.split(':')]
                date = date.replace(
                    hour=hour,
                    minute=minute,
                    second=0,
                    microsecond=0
                )

                if date.date() in hiatuses:
                    continue

                if (
                    date >= rightnow
                ) or (
                    date.date() == today and
                    include_today
                ):
                    if instance.archived:
                        return

                    if include_end_date:
                        hour, minute = [int(p) for p in end.split(':')]
                        date_end = date.replace(
                            hour=hour,
                            minute=minute,
                            second=0,
                            microsecond=0
                        ) - timedelta(seconds=1)

                        if not hour or hour < date.hour:
                            date_end += timedelta(days=1)

                        yield (
                            date,
                            date_end
                        )
                    else:
                        yield date

                    yielded += 1
                    if yielded == max:
                        return
    else:
        prev_week_number = prev_air_date.isocalendar()[1]
        valid_days = []
        i = 0

        while True:
            date = prev_air_date + timedelta(days=i)
            weekday = date.weekday()
            time = getattr(instance, '%s_start' % weekday_names[weekday])
            end = getattr(instance, '%s_end' % weekday_names[weekday])
            i += 1

            if time:
                hour, minute = [int(p) for p in time.split(':')]
                date = date.replace(
                    hour=hour,
                    minute=minute,
                    second=0,
                    microsecond=0
                )

                if date.date() in hiatuses:
                    continue

                if instance.recurrence == 14 and instance.next_air_date:
                    if date.date() < instance.next_air_date:
                        continue

                    days_between = (date.date() - instance.next_air_date).days
                    if days_between != 0 and days_between % 14 != 0:
                        continue

                if (
                    date >= rightnow
                ) or (
                    date.date() == today and
                    include_today
                ):
                    if instance.archived:
                        return

                    if include_end_date:
                        hour, minute = [int(p) for p in end.split(':')]
                        date_end = date.replace(
                            hour=hour,
                            minute=minute,
                            second=0,
                            microsecond=0
                        ) - timedelta(seconds=1)

                        if not hour or hour < date.hour:
                            date_end += timedelta(days=1)

                        yield (
                            date,
                            date_end
                        )
                    else:
                        yield date

                    yielded += 1
                    if yielded == max:
                        return

            if i >= 365:
                break


def calculate_next_air_date(instance):
    for date in calculate_next_air_dates(instance):
        return date


def search_mixcloud_for_updates():
    from .models import MixcloudSearch

    url = 'https://api.mixcloud.com/search/?q=%s&type=cloudcast&limit=100' % (
        config.MIXCLOUD_USERNAME
    )

    mixcloud_urls = []

    while True:
        response = requests.get(url)
        data = response.json()

        for search in MixcloudSearch.objects.all():
            for result in data.get('data', []):
                if re.search(
                    search.criteria,
                    result['name'],
                    re.IGNORECASE
                ) is not None:
                    mixcloud_urls.append(
                        (
                            result['url'],
                            parse_date(result['created_time']),
                            search.programme
                        )
                    )

        paging = data.get('paging')
        if paging and 'next' in paging:
            url = paging['next']
        else:
            break

    for url, date, programme in mixcloud_urls:
        if programme.updates.filter(
            kind='episode',
            url=url
        ).exists():
            continue

        programme.updates.create(
            date=date,
            url=url,
            kind='episode'
        )


def programme_on_air_now():
    from .models import Programme
    rightnow = timezone.localtime(timezone.now())

    for programme in Programme.objects.filter(archived=False):
        for (start, end) in calculate_next_air_dates(
            programme,
            max=7,
            include_today=True,
            include_end_date=True
        ):
            if start <= rightnow <= end:
                return programme


def programme_next_on_air():
    from .models import Programme

    rightnow = timezone.localtime(timezone.now())
    dates = {}

    for programme in Programme.objects.filter(archived=False):
        for date in calculate_next_air_dates(
            programme,
            max=7,
            include_today=True
        ):
            if date > rightnow:
                dates[date] = programme

    for date in sorted(dates.keys()):
        return dates[date], date

    return None, None
