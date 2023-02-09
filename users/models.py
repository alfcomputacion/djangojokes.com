from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions

# Create your models here.


def validate_avatar(value):
    h, w = get_image_dimensions(value)
    if w > 855 or h > 855:
        raise ValidationError('Image must be 855x855 pixels.')


class CustomUser(AbstractUser):
    dob = models.DateField(
        verbose_name='Date of Birth',
        null=True, blank=True
    )
    avatar = models.ImageField(upload_to='avatars/', blank=True,
                               help_text='Image must be 855px x 855px.',
                               validators=[validate_avatar])

    def get_absolute_url(self):
        return reverse('my-account')
