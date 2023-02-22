from django.contrib import admin

from .models import Joke, Category, Tag, JokeVote
from common.admin import DjangoJokesAdmin

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category

    list_display = [
        'category', 'slug', 'created', 'updated'
    ]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('slug', 'created', 'updated')
        return ()

    class Meta:
        verbose_name_plurarl = 'Categories'
        ordering = ('category',)


@admin.register(Joke)
class JokeAdmin(DjangoJokesAdmin):
    model = Joke

    #
    date_hierarchy = 'updated'
    list_display = [
        'question', 'answer', 'slug', 'created', 'updated'
    ]
    list_filter = [
        'updated', 'category', 'tags'
    ]
    ordering = ['-updated']
    search_fields = ['question', 'answer']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('slug', 'created', 'updated')
        return ()


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    model = Tag
    list_display = [
        'tag', 'slug', 'created', 'updated'
    ]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('slug', 'created', 'updated')
        return ()


@admin.register(JokeVote)
class JokeVoteAdmin(admin.ModelAdmin):
    model = JokeVote
    list_display = ['joke', 'user', 'vote']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('created', 'updated')
        return ()
