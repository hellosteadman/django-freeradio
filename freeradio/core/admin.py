from django.contrib import admin
from django_filepicker.models import FPFileField
from django_filepicker.widgets import FPFileWidget
from .models import Feature


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'ordering')

    formfield_overrides = {
        FPFileField: {
            'widget': FPFileWidget
        }
    }
