from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from model_driven.apps.graphs.utils import node_or_edge_type_edit, node_or_edit_type_new

from model_driven.apps.projects.models import Project
from .models import NodeType, EdgeType
from .forms import NodeTypeNewForm, EdgeTypeNewForm


@login_required
def graphs(request):
    context = {
        'projects': Project.objects.all(),
        'node_types': NodeType.objects.order_by('name'),
        'edge_types': EdgeType.objects.order_by('name'),
        'node_type_new_form': NodeTypeNewForm(),
        'edge_type_new_form': EdgeTypeNewForm(),
    }
    return render(request, 'graphs/graphs.html', context)


@login_required
def node_type_new(request):
    if request.method == 'POST':
        form = NodeTypeNewForm(request.POST)
        node_or_edit_type_new(request, form)

        return redirect('graphs:graphs')


@login_required
def node_type_edit(request):
    id = request.POST.get('editNodeTypeId', '')
    node_type = get_object_or_404(NodeType, pk=id)

    if request.method == 'POST':
        node_or_edge_type_edit(request, node_type)

        return redirect('graphs:graphs')


@login_required
def edge_type_new(request):
    if request.method == 'POST':
        form = EdgeTypeNewForm(request.POST)
        node_or_edit_type_new(request, form)

        return redirect('graphs:graphs')


@login_required
def edge_type_edit(request):
    id = request.POST.get('editEdgeTypeId', '')
    edge_type = get_object_or_404(EdgeType, pk=id)

    if request.method == 'POST':
        node_or_edge_type_edit(request, edge_type)

        return redirect('graphs:graphs')
