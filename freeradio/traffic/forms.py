from __future__ import absolute_import
from django import forms
from suit_redactor.widgets import RedactorWidget
from .models import Programme


class ProgrammeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProgrammeForm, self).__init__(*args, **kwargs)

        days = {
            'mon': 'Monday',
            'tue': 'Tuesday',
            'wed': 'Wednesday',
            'thu': 'Thursday',
            'fri': 'Friday',
            'sat': 'Saturday',
            'sun': 'Sunday'
        }

        for day, label in days.items():
            self.fields['%s_start' % day] = forms.RegexField(
                label=u'%s start' % label,
                required=False,
                regex=r'\d{2}:\d{2}'
            )

            self.fields['%s_end' % day] = forms.RegexField(
                label=u'End',
                required=False,
                regex=r'\d{2}:\d{2}'
            )

        self.fields['slug'].required = False
        self.fields['next_air_date'].required = False
        self.fields['monthly_number'].label = u'Recurrs monthly on the'
        self.fields['monthly_weekday'].label = u''

    class Meta:
        model = Programme
        fields = (
            'name',
            'slug',
            'subtitle',
            'series',
            'mon_start',
            'mon_end',
            'tue_start',
            'tue_end',
            'wed_start',
            'wed_end',
            'thu_start',
            'thu_end',
            'fri_start',
            'fri_end',
            'sat_start',
            'sat_end',
            'sun_start',
            'sun_end',
            'recurrence',
            'monthly_number',
            'monthly_weekday',
            'next_air_date',
            'archived',
            'banner',
            'logo'
        )

        widgets = {
            'description': RedactorWidget
        }
