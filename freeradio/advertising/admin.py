from django.contrib import admin
from django_filepicker.models import FPFileField
from django_filepicker.widgets import FPFileWidget
from .models import Advert, Placement


class PlacementInline(admin.TabularInline):
    model = Placement
    extra = 0


@admin.register(Advert)
class AdvertAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')
    inlines = (PlacementInline,)

    formfield_overrides = {
        FPFileField: {
            'widget': FPFileWidget
        }
    }
