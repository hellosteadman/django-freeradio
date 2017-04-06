from django.contrib import admin
from .models import Advert, Placement


class PlacementInline(admin.TabularInline):
    model = Placement
    extra = 0


@admin.register(Advert)
class AdvertAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')
    inlines = (PlacementInline,)
