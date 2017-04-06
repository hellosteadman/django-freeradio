from django.contrib import admin
from .models import *


@admin.register(Presenter)
class PresenterAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    list_filter = ('alumnus',)
    prepopulated_fields = {
        'slug': ('name',)
    }
