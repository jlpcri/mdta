from django import forms
from django.forms import ModelForm
from django.shortcuts import get_object_or_404
from mdta.apps.users.models import HumanResource
from mdta.apps.runner.models import TestServers

from .models import Project, Module, CatalogItem, Language


class ProjectForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['test_header'].queryset = Module.objects.filter(project=None)
        self.fields['test_header'].label_from_instance = lambda obj: "%s" % obj.name
        self.fields['testrail'].label_from_instance = lambda obj: "%s" % obj.project_name
        # self.fields['catalog'].queryset = CatalogItem.objects.select_related('parent').all()
        for field_name in ['lead']:
            self.fields[field_name].queryset = HumanResource.objects.select_related('user').all().exclude(user__username='admin')
            self.fields[field_name].label_from_instance = lambda obj: "%s %s" % (obj.user.first_name, obj.user.last_name)

        # for field in self.fields:
        #     if field == 'archive':
        #         continue
        #     help_text = self.fields[field].help_text
        #     self.fields[field].help_text = None
        #     if help_text != '':
        #         self.fields[field].widget.attrs.update({
        #             'class': 'form-control',
        #             'data-toggle': 'tooltip',
        #             'data-placement': 'top',
        #             'title': help_text
        #         })
        #     else:
        #         self.fields[field].widget.attrs.update({
        #             'class': 'form-control',
        #         })

    class Meta:
        model = Project
        fields = ['name', 'test_header', 'version', 'testrail', 'lead']
        exclude = ['created', 'updated', 'members']
        widgets = {
            'name': forms.TextInput(),
            'test_header': forms.Select(),
            'version': forms.TextInput(),
            'catalog': forms.SelectMultiple(attrs={'size': '10'}),
            'testrail': forms.Select(),
            'lead': forms.Select(),
            'members': forms.SelectMultiple(attrs={'size': '6'})
        }


class ModuleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        project_id = kwargs.pop('project_id', '')
        super(ModuleForm, self).__init__(*args, **kwargs)
        if project_id:
            # project = get_object_or_404(Project, pk=project_id)
            self.fields['project'].queryset = Project.objects.filter(pk=project_id)
            # self.fields['catalog'].queryset = project.catalog.all()

        self.fields['project'].empty_label = None
        # self.fields['catalog'].queryset = CatalogItem.objects.select_related('parent').all()

        for field in self.fields:
            help_text = self.fields[field].help_text
            self.fields[field].help_text = None
            if help_text != '':
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'data-toggle': 'tooltip',
                    'data-placement': 'top',
                    'title': help_text
                })
            else:
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                })

    class Meta:
        model = Module
        fields = ['project', 'name']
        widgets = {
            'project': forms.Select(),
            'name': forms.TextInput(),
            # 'catalog': forms.SelectMultiple(attrs={
            #     'class': 'form-control',
            #     'size': '10'
            # }),
        }


class TestHeaderForm(ModelForm):
    class Meta:
        model = Module
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class TestRunnerForm(forms.Form):
    TEST_CHOICES = [[x.server, x.name] for x in TestServers.objects.all()]

    browser = forms.CharField(max_length=100,
                                  widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "linux5578"}))

    apn = forms.CharField(max_length=50,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '4061702'}))

    testserver = forms.ChoiceField(choices=TEST_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    suite = forms.CharField(widget=forms.HiddenInput(attrs={'id': 'suiteid'}), required=False, max_length=50)


class ProjectConfigForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProjectConfigForm, self).__init__(*args, **kwargs)
        self.fields['test_header'].queryset = Module.objects.filter(project=None)
        self.fields['language'].queryset = Language.objects.filter(project=self.instance)

        self.fields['test_header'].label_from_instance = lambda obj: "%s" % obj.name
        self.fields['testrail'].label_from_instance = lambda obj: "%s" % obj.project_name
        self.fields['language'].label_from_instance = lambda obj: "%s" % obj.name

        for field in self.fields:
            if field == 'archive':
                continue
            help_text = self.fields[field].help_text
            self.fields[field].help_text = None
            if help_text != '':
                self.fields[field].widget.attrs.update(
                    {'class': 'form-control', 'data-toggle': 'tooltip', 'data-placement': 'top', 'title': help_text})
            else:
                self.fields[field].widget.attrs.update({'class': 'form-control', })

    class Meta:
        model = Project
        fields = ['name', 'test_header', 'testrail', 'language', 'version', 'archive']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',
                                           'readonly': True}),
            'test_header': forms.Select(attrs={'class': 'form-control'}),
            'testrail': forms.Select(attrs={'class': 'form-control'}),
            'language': forms.Select(attrs={'class': 'form-control'}),
            'version': forms.TextInput(attrs={'class': 'form-control'}),
        }


class LanguageNewForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(LanguageNewForm, self).__init__(*args, **kwargs)
        self.fields['project'].empty_label = None

    class Meta:
        model = Language
        fields = ['project', 'name', 'root_path']
        widgets = {
            'project': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'root_path': forms.TextInput(attrs={'class': 'form-control'}),
        }


class UploadForm(forms.Form):
    file = forms.FileField(max_length=100, required=True)

    class Meta:
        model = Module
