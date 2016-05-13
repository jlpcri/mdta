from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
import json

from model_driven.apps.projects.models import Project
from .models import NodeType, EdgeType
from .forms import NodeTypeNewForm, EdgeTypeNewForm


@login_required
def graphs(request):
    context = {
        'projects': Project.objects.all(),
        'node_types': NodeType.objects.all(),
        'edge_types': EdgeType.objects.all(),
        'node_type_new_form': NodeTypeNewForm(),
        'edge_type_new_form': EdgeTypeNewForm(),
    }
    return render(request, 'graphs/graphs.html', context)


@login_required
def node_type_new(request):
    if request.method == 'POST':
        form = NodeTypeNewForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Node Type is added.')
        else:
            messages.error(request, 'Add Node Type Errors found.')

        return redirect('graphs:graphs')


@login_required
def node_type_edit(request):
    if request.method == 'POST':
        id = request.POST.get('editNodeTypeId', '')
        name = request.POST.get('editNodeTypeName', '')
        keys = request.POST.getlist('editNodeTypeKeys', '')

        node_type = get_object_or_404(NodeType, pk=id)
        try:
            node_type.name = name
            node_type.keys = keys[0].split(',')
            node_type.save()
        except (ValidationError, IntegrityError):
            messages.error(request, 'Edit Node Type Error')

        return redirect('graphs:graphs')


@login_required
def edge_type_new(request):
    if request.method == 'POST':
        form = EdgeTypeNewForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Edge Type is added.')
        else:
            messages.error(request, 'Add Edge Type Errors found.')

        return redirect('graphs:graphs')


@login_required
def edge_type_edit(request):
    pass
