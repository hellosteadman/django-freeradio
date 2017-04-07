from django_filepicker.widgets import FPFileWidget
from django import forms
from suit_redactor.widgets import RedactorWidget


class SeriesForm(forms.ModelForm):
    class Meta:
        widgets = {
            'description': RedactorWidget,
            'artwork': FPFileWidget,
            'banner': FPFileWidget
        }
