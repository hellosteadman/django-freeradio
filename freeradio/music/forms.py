from suit_redactor.widgets import RedactorWidget
from django import forms


class TrackForm(forms.ModelForm):
    class Meta:
        widgets = {
            'notes': RedactorWidget
        }
