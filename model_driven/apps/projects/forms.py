from django import forms
from django.forms import ModelForm

from .models import Project


class ProjectNewForm(ModelForm):
    class Meta:
        model = Project
        exclude = ['created', 'updated']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'lead': forms.Select(attrs={'class': 'form-control'}),
            'worker': forms.SelectMultiple(attrs={'class': 'form-control'})
        }
