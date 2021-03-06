from django import forms
from django.forms import ModelForm

from mdta.apps.projects.models import TestRailConfiguration, TestRailInstance
from mdta.apps.testcases.utils import get_projects_from_testrail


class TestrailConfigurationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(TestrailConfigurationForm, self).__init__(*args, **kwargs)
        names = ()
        testrail_instance = TestRailInstance.objects.filter(username='testrail@west.com')
        if testrail_instance.count() > 0:
            self.fields['instance'].queryset = testrail_instance
            self.fields['instance'].empty_label = None
            self.fields['instance'].label_from_instance = lambda obj: "%s" % obj.host

            try:
                testrail_projects = get_projects_from_testrail(testrail_instance[0])
            except Exception as e:
                testrail_projects = []
                print(e)
            for item in testrail_projects:
                names += ((item['name'], item['name']), )

            self.fields['project_name'] = forms.ChoiceField(
                choices=sorted(names, key=lambda tup: tup[1]),
                widget=forms.Select(attrs={'class': 'form-control'})
            )

    class Meta:
        model = TestRailConfiguration
        exclude = ['project_id', 'test_suite']
        widgets = {
            'instance': forms.Select(attrs={'class': 'form-control'}),
        }

