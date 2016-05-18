from django import forms
from django.forms import ModelForm


from .models import NodeType, Node, EdgeType, Edge
from model_driven.apps.projects.models import Project


class NodeTypeNewForm(ModelForm):
    class Meta:
        model = NodeType
        fields = ['name', 'keys']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'keys': forms.TextInput(attrs={'class': 'form-control'}),
        }


class NodeNewForm(ModelForm):
    def __init__(self, *args, **kwargs):
        project_id = kwargs.pop('project_id')
        super(NodeNewForm, self).__init__(*args, **kwargs)
        if project_id:
            self.fields['project'].queryset = Project.objects.filter(pk=project_id)
            self.fields['parent'].queryset = Node.objects.filter(project__id=project_id)
            for field_name in ['project', 'parent', 'type']:
                self.fields[field_name].empty_label = None

    class Meta:
        model = Node
        fields = ['project', 'type', 'parent', 'name']
        widgets = {
            'project': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'parent': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class EdgeTypeNewForm(ModelForm):
    class Meta:
        model = EdgeType
        fields = ['name', 'keys']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'keys': forms.TextInput(attrs={'class': 'form-control'}),
        }
