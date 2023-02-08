from datetime import datetime
from django import forms

from django.core.exceptions import ValidationError

from .models import Applicant


def validate_checked(value):
    if not value:
        raise ValidationError(
            message='You must accept the terms'
        )


class JobApplicationForm(forms.ModelForm):
    DAYS = (
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday')
    )

    available_days = forms.TypedMultipleChoiceField(
        choices=DAYS,
        coerce=int,
        help_text='Check all days that you can work.',
        widget=forms.CheckboxSelectMultiple(
            attrs={'checked': True}
        )
    )
    confirmation = forms.BooleanField(
        label='I certify that the information I have provided is true.',
        validators=[validate_checked]
    )

    class Meta:
        model = Applicant
        fields = (
            'first_name', 'last_name', 'email', 'website', 'employment_type',
            'start_date', 'available_days', 'desired_hourly_wage',
            'cover_letter', 'resume', 'confirmation', 'job'
        )
        widgets = {
            'first_name': forms.TextInput(attrs={'autofocus': True}),
            'website': forms.TextInput(
                attrs={'placeholder': 'https://www.example.com'}
            ),
            'start_date': forms.SelectDateWidget(
                attrs={'style': 'width: 31%; display: inline-block; margin: 0 1%'},
                years=range(datetime.now().year, datetime.now().year+2)
            ),
            'cover_letter': forms.Textarea(attrs={'cols': '100', 'rows': '5'}),

            'resume': forms.FileInput(attrs={'accept': 'application/pdf'}),

        }
        error_messages = {
            'start_date': {
                'past_date': 'Please enter a future date.'
            }
        }