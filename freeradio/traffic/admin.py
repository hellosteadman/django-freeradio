from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from .models import *
from .helpers import calculate_next_air_date
from .forms import ProgrammeForm


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {
        'slug': ('name',)
    }


class ProgrammePresenterInline(admin.TabularInline):
    model = ProgrammePresenter
    extra = 0


class ProgrammeHiatusInline(admin.TabularInline):
    model = ProgrammeHiatus
    extra = 0


class MixcloudSearch(admin.TabularInline):
    model = MixcloudSearch
    extra = 0


class ProgrammeStatusFilter(admin.SimpleListFilter):
    title = _('Status')
    parameter_name = 'archived'

    def lookups(self, request, model_admin):
        return (
            (None, _('Active')),
            ('archived', _('Archived')),
            ('all', _('All')),
        )

    def choices(self, cl):
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == lookup,
                'query_string': cl.get_query_string(
                    {
                        self.parameter_name: lookup
                    },
                    []
                ),
                'display': title
            }

    def queryset(self, request, queryset):
        value = self.value()
        if value is None:
            return queryset.filter(archived=False)

        if value == 'archived':
            return queryset.filter(archived=True)

        return queryset


@admin.register(Programme)
class ProgrammeAdmin(admin.ModelAdmin):
    list_display = ('_name', '_presenters', '_tx_dates', '_next_air_date')
    search_fields = ('name', 'presenters__name')
    list_filter = (ProgrammeStatusFilter, 'recurrence', 'presenters')

    prepopulated_fields = {
        'slug': ('name',)
    }

    fieldsets = (
        (
            None,
            {
                'fields': (
                    'name',
                    'slug',
                    'subtitle',
                    'description',
                    'series'
                )
            }
        ),
        (
            u'Recurrence and airings',
            {
                'fields': (
                    ('mon_start', 'mon_end'),
                    ('tue_start', 'tue_end'),
                    ('wed_start', 'wed_end'),
                    ('thu_start', 'thu_end'),
                    ('fri_start', 'fri_end'),
                    ('sat_start', 'sat_end'),
                    ('sun_start', 'sun_end'),
                    (
                        'recurrence',
                        'monthly_number',
                        'monthly_weekday'
                    ),
                    'next_air_date',
                    'archived'
                ),
                'description': (
                    'Add weekly air times (in HH:MM format), '
                    'specify the recurrence pattern and set the '
                    'next transmission date for the programme.'
                )
            }
        ),
        (
            u'Media',
            {
                'fields': (
                    'banner',
                    'logo'
                )
            }
        )
    )

    inlines = [
        ProgrammePresenterInline,
        ProgrammeHiatusInline,
        MixcloudSearch
    ]

    form = ProgrammeForm

    def get_queryset(self, request):
        queryset = super(ProgrammeAdmin, self).get_queryset(request)

        if not request.user.has_perm('traffic.add_programme'):
            queryset = queryset.filter(
                presenters__user=request.user
            ).distinct()

        return queryset

    def _name(self, obj):
        return str(obj)

    def _tx_dates(self, obj):
        return obj.get_tx_display()

    def _presenters(self, obj):
        return obj.get_presenters_display()

    def _next_air_date(self, obj):
        return calculate_next_air_date(obj)


@admin.register(Update)
class UpdateAdmin(admin.ModelAdmin):
    list_display = ('title', 'programme', 'date', 'kind')
    list_filter = ('programme', 'kind')
    fields = (
        'programme',
        'kind',
        'date',
        'title',
        'author',
        'description',
        'url'
    )

    def get_form(self, request, obj, **kwargs):
        form = super(UpdateAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['date'].initial = timezone.localtime(
            timezone.now()
        )

        return form

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'author':
            kwargs['initial'] = request.user.pk
        elif not request.user.has_perm('traffic.add_programme'):
            if db_field.name == 'programme':
                kwargs['queryset'] = (
                    db_field.related_model._default_manager.filter(
                        presenters__user=request.user
                    ).distinct()
                )

        return super(UpdateAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )

    def get_queryset(self, request):
        queryset = super(UpdateAdmin, self).get_queryset(request)

        if not request.user.has_perm('traffic.add_programme'):
            queryset = queryset.filter(
                programme__presenters__user=request.user
            ).distinct()

        return queryset


class LookaheadItemInline(admin.TabularInline):
    model = LookaheadItem
    extra = 0


@admin.register(Lookahead)
class LookaheadAdmin(admin.ModelAdmin):
    list_display = ('start',)
    inlines = [LookaheadItemInline]
