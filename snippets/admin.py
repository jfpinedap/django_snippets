"""Snippet Admin"""

from django.contrib import admin

from .models import Language, Snippet


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)

@admin.register(Snippet)
class SnippetAdmin(admin.ModelAdmin):
    pass