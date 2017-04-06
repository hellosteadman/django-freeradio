from django.db.models import Manager
from django.utils import timezone
from datetime import timedelta
from .helpers import calculate_next_air_dates


class ProgrammeManager(Manager):
    def get_schedule(self, weekday=None):
        rightnow = timezone.localtime(timezone.now()).replace(
            hour=0,
            minute=0,
            second=0
        )

        if weekday is None:
            weekday = rightnow.weekday()

        include_today = rightnow.weekday() == weekday
        while rightnow.weekday() != weekday:
            rightnow += timedelta(days=1)

        timeslots = {}
        for programme in self.filter(archived=False):
            for date in calculate_next_air_dates(
                programme,
                max=7,
                include_today=True
            ):
                if date.year == rightnow.year:
                    if date.month == rightnow.month:
                        if date.day == rightnow.day:
                            timeslots[date.strftime('%H:%I')] = (
                                date,
                                programme
                            )

                            break

        for key in sorted(timeslots.keys()):
            yield timeslots[key]
