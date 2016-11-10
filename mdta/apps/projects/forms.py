from django import forms
from django.forms import ModelForm
from django.shortcuts import get_object_or_404
from mdta.apps.users.models import HumanResource

from .models import Project, Module, CatalogItem


class ProjectForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['test_header'].queryset = Module.objects.filter(project=None)

        self.fields['test_header'].label_from_instance = lambda obj: "%s" % obj.name
        self.fields['testrail'].label_from_instance = lambda obj: "%s" % obj.project_name
        self.fields['catalog'].queryset = CatalogItem.objects.select_related('parent').all()
        for field_name in ['lead', 'members']:
            self.fields[field_name].queryset = HumanResource.objects.select_related('user').all().exclude(user__username='admin')
            self.fields[field_name].label_from_instance = lambda obj: "%s %s" % (obj.user.first_name, obj.user.last_name)

    class Meta:
        model = Project
        exclude = ['created', 'updated']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'test_header': forms.Select(attrs={'class': 'form-control'}),
            'version': forms.TextInput(attrs={'class': 'form-control'}),
            'catalog': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'size': '10'
            }),
            'testrail': forms.Select(attrs={'class': 'form-control'}),
            'lead': forms.Select(attrs={'class': 'form-control'}),
            'members': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'size': '6'
            })
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
        self.fields['catalog'].queryset = CatalogItem.objects.select_related('parent').all()

    class Meta:
        model = Module
        fields = ['project', 'name', 'catalog']
        widgets = {
            'project': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'catalog': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'size': '10'
            }),
        }


class TestHeaderForm(ModelForm):
    class Meta:
        model = Module
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ProjectConfigForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProjectConfigForm, self).__init__(*args, **kwargs)
        self.fields['test_header'].queryset = Module.objects.filter(project=None)

        self.fields['test_header'].label_from_instance = lambda obj: "%s" % obj.name
        self.fields['testrail'].label_from_instance = lambda obj: "%s" % obj.project_name

    class Meta:
        model = Project
        fields = ['name', 'test_header', 'testrail', 'version']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',
                                           'readonly': True}),
            'test_header': forms.Select(attrs={'class': 'form-control'}),
            'testrail': forms.Select(attrs={'class': 'form-control'}),
            'version': forms.TextInput(attrs={'class': 'form-control'}),
        }
