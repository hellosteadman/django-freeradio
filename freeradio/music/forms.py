from django_filepicker.widgets import FPFileWidget
from suit_redactor.widgets import RedactorWidget
from django import forms


class TrackForm(forms.ModelForm):
    class Meta:
        widgets = {
            'notes': RedactorWidget,
            'artwork': FPFileWidget
        }
