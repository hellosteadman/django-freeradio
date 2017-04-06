from django.contrib import admin
from django.utils import timezone
from .models import *
from .forms import *


class SeriesPresenterInline(admin.TabularInline):
    model = SeriesPresenter
    extra = 0


class SubscriptionLinkInline(admin.TabularInline):
    model = SubscriptionLink
    extra = 0


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'presenters')
    prepopulated_fields = {
        'slug': ('name',)
    }

    inlines = [
        SeriesPresenterInline,
        SubscriptionLinkInline
    ]

    form = SeriesForm

    fieldsets = (
        (
            None,
            {
                'fields': ('name', 'slug', 'url', 'public')
            }
        ),
        (
            u'Feed details',
            {
                'fields': (
                    'subtitle',
                    'author',
                    'artwork'
                )
            }
        ),
        (
            u'Web details',
            {
                'fields': (
                    'description',
                    'banner'
                )
            }
        )
    )

    def get_queryset(self, request):
        queryset = super(SeriesAdmin, self).get_queryset(request)

        if not request.user.has_perm('podcasting.add_series'):
            queryset = queryset.filter(
                presenters__user=request.user
            ).distinct()

        return queryset

    def presenters(self, obj):
        return obj.get_presenters_display()
