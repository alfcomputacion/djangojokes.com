from django.contrib import admin

from .models import Joke, Category

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
class JokeAdmin(admin.ModelAdmin):
    model = Joke

    list_display = [
        'question', 'answer', 'slug', 'created', 'updated'
    ]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('slug', 'created', 'updated')
        return ()
