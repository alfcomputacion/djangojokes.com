import filetype
from datetime import datetime
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db import models

# Create your models here.


def validate_future_date(value):
    if value < datetime.now().date():
        raise ValidationError(
            message=f'{value} is in the past.', code='past_date'
        )


def validate_pdf(value):
    kind = filetype.guess(value)
    if not kind or kind.mime != 'application/pdf':
        raise ValidationError("That's not a PDF file")


class Job(models.Model):
    title = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Applicant(models.Model):
    EMPLOYMENT_TYPES = (
        (None, '----Please Choose----'),
        ('ft', 'Full Time'),
        ('pt', 'Part Time'),
        ('contract', 'Contract Work')
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(help_text='A valid email')
    website = models.URLField(
        blank=True, validators=[URLValidator(schemes=['http', 'https'])]
    )
    employment_type = models.CharField(
        max_length=10, choices=EMPLOYMENT_TYPES
    )
    start_date = models.DateField(
        help_text='The earliest you can start working',
        validators=[validate_future_date]
    )
    avaliable_days = models.CharField(max_length=20)
    desired_hourly_wage = models.DecimalField(max_digits=5, decimal_places=2)
    cover_letter = models.TextField()
    resume = models.FileField(
        upload_to='private/resumes', blank=True, help_text='PDFs only',
        validators=[validate_pdf]
    )
    confirmation = models.BooleanField()
    job = models.ForeignKey('Job', on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.job}).'
