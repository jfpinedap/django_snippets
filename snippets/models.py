"""Snippets Mdels"""

# Base imports
from __future__ import unicode_literals
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.styles import get_style_by_name
from pygments.formatters import HtmlFormatter
from django.contrib.humanize.templatetags.humanize import naturaltime

# Django imports
from django.db import models
from django.contrib.auth.models import User


class Language(models.Model):
    """
    Language Class
    """
    name = models.CharField(max_length=50, blank=False, null=False)
    slug = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return self.name


class Snippet(models.Model):
    """
    Snippet Class
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False, null=False
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=True)
    snippet = models.TextField(blank=False, null=False)
    language = models.ForeignKey(
        Language,
        on_delete=models.CASCADE,
        related_name='language',
        blank=False,
        null=False
    )
    public = models.BooleanField(default=False)

    def pygmented(self):
        """
        Returns the snippet pygmented on its corresponding language
        """
        lexer = get_lexer_by_name(self.language.slug, stripall=True)
        formatter = HtmlFormatter(
            linenos=True,
            style=get_style_by_name('colorful')
        )
        return highlight(self.snippet, lexer, formatter)

    def natural_created(self):
        """
        Returns the natural format of created date time
        """
        return naturaltime(self.created)


    def __str__(self):
        return self.name
    class Meta:
        ordering = ("-created",)
