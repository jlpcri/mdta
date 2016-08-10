from django import forms
from django.forms import ModelForm
from django.shortcuts import get_object_or_404

from .models import Project, Module, CatalogItem


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        exclude = ['created', 'updated']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'catalog': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'testrail': forms.Select(attrs={'class': 'form-control'}),
            'lead': forms.Select(attrs={'class': 'form-control'}),
            'members': forms.SelectMultiple(attrs={'class': 'form-control'})
        }


class ModuleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        project_id = kwargs.pop('project_id', '')
        super(ModuleForm, self).__init__(*args, **kwargs)
        if project_id:
            project = get_object_or_404(Project, pk=project_id)
            self.fields['project'].queryset = Project.objects.filter(pk=project_id)
            self.fields['catalog'].queryset = project.catalog.all()

        self.fields['project'].empty_label = None

    class Meta:
        model = Module
        fields = ['project', 'name', 'catalog']
        widgets = {
            'project': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'catalog': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
