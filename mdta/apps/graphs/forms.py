from django import forms
from django.forms import ModelForm
from django.shortcuts import get_object_or_404

from .models import NodeType, Node, EdgeType, Edge
from mdta.apps.projects.models import Project, Module


class NodeTypeNewForm(ModelForm):
    class Meta:
        model = NodeType
        exclude = []
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'keys': forms.TextInput(attrs={'class': 'form-control'}),
            'subkeys': forms.TextInput(attrs={'class': 'form-control'}),
        }


class NodeNewForm(ModelForm):
    def __init__(self, *args, **kwargs):
        project_id = kwargs.pop('project_id', '')
        module_id = kwargs.pop('module_id', '')
        super(NodeNewForm, self).__init__(*args, **kwargs)
        if project_id:
            self.fields['module'].queryset = Module.objects.filter(project__id=project_id)
        elif module_id:
            self.fields['module'].queryset = Module.objects.filter(pk=module_id)

        for field_name in ['module', 'type']:
            self.fields[field_name].empty_label = None
            self.fields[field_name].label_from_instance = lambda obj: "%s" % obj.name

    class Meta:
        model = Node
        fields = ['module', 'type', 'name']
        widgets = {
            'module': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class EdgeTypeNewForm(ModelForm):
    class Meta:
        model = EdgeType
        exclude = []
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'keys': forms.TextInput(attrs={'class': 'form-control'}),
            'subkeys': forms.TextInput(attrs={'class': 'form-control'}),
        }


class EdgeNewForm(ModelForm):
    def __init__(self, *args, **kwargs):
        project_id = kwargs.pop('project_id', '')
        module_id = kwargs.pop('module_id', '')
        super(EdgeNewForm, self).__init__(*args, **kwargs)
        if project_id:
            self.fields['from_node'].queryset = Node.objects.filter(module__project__id=project_id)
            self.fields['to_node'].queryset = Node.objects.filter(module__project__id=project_id)
        elif module_id:
            self.fields['from_node'].queryset = Node.objects.filter(module__id=module_id)
            self.fields['to_node'].queryset = Node.objects.filter(module__id=module_id)

        for field_name in ['from_node', 'to_node', 'type']:
            self.fields[field_name].empty_label = None
            self.fields[field_name].label_from_instance = lambda obj: "%s" % obj.name

    class Meta:
        model = Edge
        fields = ['type', 'from_node', 'to_node', 'priority']
        widgets = {
            'type': forms.Select(attrs={'class': 'form-control'}),
            'from_node': forms.Select(attrs={'class': 'form-control'}),
            'to_node': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
        }


class EdgeAutoNewForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EdgeAutoNewForm, self).__init__(*args, **kwargs)
        self.fields['type'].empty_label = None
        self.fields['type'].label_from_instance = lambda obj: "%s" % obj.name

    class Meta:
        model = Edge
        fields = ['type', 'priority']
        widgets = {
            'type': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_edge_type'
            }),
            'priority': forms.Select(attrs={'class': 'form-control'}),
        }
