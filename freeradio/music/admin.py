from django.contrib import admin
from .models import *
from .forms import *


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist')
    form = TrackForm


class PlaylistTrackInline(admin.TabularInline):
    model = PlaylistTrack
    extra = 0


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_dipslay = ('name',)
    prepopulated_fields = {
        'slug': ('name',)
    }

    inlines = [PlaylistTrackInline]
