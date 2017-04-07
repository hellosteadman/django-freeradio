from django_filepicker.widgets import FPFileWidget
from django import forms
from suit_redactor.widgets import RedactorWidget


class PresenterForm(forms.ModelForm):
    class Meta:
        widgets = {
            'biography': RedactorWidget,
            'photo': FPFileWidget
        }
