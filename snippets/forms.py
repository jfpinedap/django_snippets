"""Snippet Froms"""

# Django Imports
from django import forms

# App imports
from .models import Snippet


class SnippetForm(forms.ModelForm):
    """
    Snippet Add From
    """

    class Meta:
        model = Snippet

        fields = [
            'name', 'description', 'snippet',
            'language', 'public'
        ]

        labels = {
            'name': 'Nombre',
            'description': 'Descripción',
            'snippet': 'Snippet',
            'language': 'Lenguaje',
            'public': 'Público',
        }

        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Nombre del snippet'}
            ),
            'description': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Descripción del snippet'}
            ),
            'language': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'snippet': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Ingrese aquí el snippet que desea crear'}
            ),
        }