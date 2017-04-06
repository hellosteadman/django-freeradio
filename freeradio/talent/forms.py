from django import forms
from suit_redactor.widgets import RedactorWidget


class PresenterForm(forms.ModelForm):
    class Meta:
        widgets = {
            'biography': RedactorWidget
        }
