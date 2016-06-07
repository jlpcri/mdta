from django import forms
from django.forms import ModelForm

from .models import Project, Module


class ProjectNewForm(ModelForm):
    class Meta:
        model = Project
        exclude = ['created', 'updated']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'lead': forms.Select(attrs={'class': 'form-control'}),
            'members': forms.SelectMultiple(attrs={'class': 'form-control'})
        }


class ModuleNewForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModuleNewForm, self).__init__(*args, **kwargs)
        self.fields['project'].empty_label = None

    class Meta:
        model = Module
        fields = ['project', 'name']
        widgets = {
            'project': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
