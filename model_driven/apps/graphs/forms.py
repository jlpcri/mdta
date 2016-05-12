from django import forms
from django.forms import ModelForm


from .models import NodeType, Node, EdgeType, Edge


class NodeTypeNewForm(ModelForm):
    class Meta:
        model = NodeType
        fields = ['name', 'keys']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'keys': forms.TextInput(attrs={'class': 'form-control'}),
        }


class EdgeTypeNewForm(ModelForm):
    class Meta:
        model = EdgeType
        fields = ['name', 'keys']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'keys': forms.TextInput(attrs={'class': 'form-control'}),
        }
