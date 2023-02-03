from django.db import models
from django.urls import reverse
from common.utils.text import unique_slug
# Create your models here.


class Category(models.Model):
    category = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150, unique=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category

    def get_absolute_url(self):
        return reverse('jokes:category', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            value = str(self)
            self.slug = unique_slug(value, type(self))
        super().save(*args, **kwargs)


class Joke(models.Model):
    question = models.CharField(max_length=100)
    answer = models.CharField(max_length=150)
    category = models.ForeignKey(
        'Category', related_name='jokes', on_delete=models.PROTECT)
    slug = models.SlugField(max_length=50, unique=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question

    def save(self, *args, **kwargs):
        if not self.slug:
            value = str(self)
            self.slug = unique_slug(value, type(self))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('jokes:detail', args=[self.slug])
