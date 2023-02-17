from django.db import models
from django.urls import reverse
from common.utils.text import unique_slug

from django.conf import settings
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

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ('category',)


class Joke(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.PROTECT)
    question = models.CharField(max_length=100)
    answer = models.CharField(max_length=150)
    category = models.ForeignKey(
        'Category', related_name='jokes', on_delete=models.PROTECT)
    tags = models.ManyToManyField('Tag', blank=True, related_name='jokes')
    slug = models.SlugField(max_length=50, unique=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def num_votes(self):
        return self.jokevotes.count()

    @property
    def num_likes(self):
        return self.jokevotes.filter(vote=1).count()

    @property
    def num_dislikes(self):
        return self.jokevotes.filter(vote=-1).count()

    def __str__(self):
        return self.question

    def save(self, *args, **kwargs):
        if not self.slug:
            value = str(self)
            self.slug = unique_slug(value, type(self))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('jokes:detail', args=[self.slug])


class Tag(models.Model):
    tag = models.CharField(max_length=50)
    slug = models.SlugField(
        max_length=50, unique=True, editable=False, null=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('jokes:tag', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            value = str(self)
            self.slug = unique_slug(value, type(self))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.tag


class JokeVote(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='jokevotes'
    )
    joke = models.ForeignKey(
        Joke, on_delete=models.CASCADE,
        related_name='jokevotes'
    )
    vote = models.SmallIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'joke'], name='one_vote_per_user_per_joke'
            )
        ]
