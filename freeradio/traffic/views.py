from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from datetime import timedelta
from .models import Programme, Update, Lookahead
from ..core.mixins import BootstrapMixin


class ScheduleView(BootstrapMixin, TemplateView):
    template_name = 'traffic/schedule.html'
    title_parts = ['Schedule']

    def get_body_classes(self):
        rightnow = timezone.localtime(timezone.now())
        today = (
            'mon',
            'tue',
            'wed',
            'thu',
            'fri',
            'sat',
            'sun'
        )[rightnow.weekday()]
        selected_day = self.kwargs.get('day', today)

        return (
            'traffic',
            'schedule',
            'schedule-%s' % selected_day
        )

    def get_context_data(self, **kwargs):
        context = super(ScheduleView, self).get_context_data(**kwargs)
        rightnow = timezone.localtime(timezone.now())
        today = (
            'mon',
            'tue',
            'wed',
            'thu',
            'fri',
            'sat',
            'sun'
        )[rightnow.weekday()]

        selected_day = kwargs.get('day', today)
        days = (
            {
                'slug': 'mon',
                'name': 'Monday',
                'selected': selected_day == 'mon',
                'url': reverse('traffic:schedule_day', args=['mon'])
            },
            {
                'slug': 'tue',
                'name': 'Tuesday',
                'selected': selected_day == 'tue',
                'url': reverse('traffic:schedule_day', args=['tue'])
            },
            {
                'slug': 'wed',
                'name': 'Wednesday',
                'selected': selected_day == 'wed',
                'url': reverse('traffic:schedule_day', args=['wed'])
            },
            {
                'slug': 'thu',
                'name': 'Thursday',
                'selected': selected_day == 'thu',
                'url': reverse('traffic:schedule_day', args=['thu'])
            },
            {
                'slug': 'fri',
                'name': 'Friday',
                'selected': selected_day == 'fri',
                'url': reverse('traffic:schedule_day', args=['fri'])
            },
            {
                'slug': 'sat',
                'name': 'Saturday',
                'selected': selected_day == 'sat',
                'url': reverse('traffic:schedule_day', args=['sat'])
            },
            {
                'slug': 'sun',
                'name': 'Sunday',
                'selected': selected_day == 'sun',
                'url': reverse('traffic:schedule_day', args=['sun'])
            }
        )

        context['days'] = days
        schedule = list(
            Programme.objects.get_schedule(
                {
                    'mon': 0,
                    'tue': 1,
                    'wed': 2,
                    'thu': 3,
                    'fri': 4,
                    'sat': 5,
                    'sun': 6
                }[selected_day]
            )
        )

        lookahead_start = rightnow.date()
        lookahead_end = rightnow.date()

        while lookahead_start.weekday():
            lookahead_start -= timedelta(days=1)

        lookahead_end = lookahead_start + timedelta(days=6)
        lookaheads = Lookahead.objects.exclude(
            start__lt=lookahead_end,
            start__gt=lookahead_start
        )

        for lookahead in lookaheads:
            items = dict(
                lookahead.items.values_list(
                    'programme__pk',
                    'details'
                )
            )

            for i, (date, programme) in enumerate(schedule):
                schedule[i][1].upcoming_notes = items.get(programme.pk)

        context['schedule'] = schedule
        context['menu_selection'] = 'traffic:schedule'
        return context


class ProgrammeListView(BootstrapMixin, ListView):
    model = Programme
    body_classes = ('traffic', 'programmes')
    menu_selection = 'traffic:programmes'
    title_parts = ['Live shows']

    def get_queryset(self):
        return super(ProgrammeListView, self).get_queryset().filter(
            archived=False
        ).exclude(
            recurrence=-1
        )


class ProgrammeView(BootstrapMixin, DetailView):
    model = Programme
    body_classes = ('traffic', 'programme')
    menu_selection = 'traffic:programme'

    def get_title_parts(self):
        yield str(self.object)
        yield 'Shows'

    def get_social_image(self):
        return self.object.logo

    def get_social_description(self):
        return self.object.subtitle

    def get_context_data(self, **kwargs):
        context = super(ProgrammeView, self).get_context_data(**kwargs)
        rightnow = timezone.localtime(timezone.now())
        updates = Update.objects.filter(
            programme=kwargs['object'],
            date__lte=rightnow
        )

        paginator = Paginator(updates, 10)

        try:
            page = paginator.page(self.request.GET.get('page'))
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)

        lookahead_start = rightnow.date()
        lookahead_end = rightnow.date()

        while lookahead_start.weekday():
            lookahead_start -= timedelta(days=1)

        lookahead_end = lookahead_start + timedelta(days=6)
        lookaheads = Lookahead.objects.exclude(
            start__lt=lookahead_end,
            start__gt=lookahead_start
        )

        for lookahead in lookaheads:
            for item in lookahead.items.filter(
                programme=kwargs['object']
            ):
                context['upcoming'] = item.details
                break

        context['updates'] = page
        return context
