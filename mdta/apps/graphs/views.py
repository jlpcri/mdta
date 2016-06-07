import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from mdta.apps.graphs.utils import node_or_edge_type_edit, node_or_edit_type_new

from mdta.apps.projects.models import Project
from .models import NodeType, EdgeType, Edge
from .forms import NodeTypeNewForm, NodeNewForm, EdgeTypeNewForm, EdgeNewForm


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
def node_new(request, project_id):
    if request.method == 'GET':
        form = NodeNewForm(project_id=project_id)
    elif request.method == 'POST':
        data = {}
        form = NodeNewForm(request.POST, project_id=project_id)
        if form.is_valid():
            node = form.save(commit=False)
            for key in node.type.keys:
                data[key] = request.POST.get(key, '')
            node.data = data
            node.save()

            messages.success(request, 'Node is added.')
            return redirect('graphs:graphs')
        else:
            print(form.errors)
            messages.error(request, 'Node new Error')
    else:
        form = ''

    context = {
        'form': form,
        'project_id': project_id
    }

    return render(request, 'graphs/node_new.html', context)


@login_required
def node_edit(request):
    pass


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


@login_required
def edge_new(request, project_id):
    if request.method == 'GET':
        form = EdgeNewForm(project_id=project_id)
    elif request.method == 'POST':
        data = {}
        form = EdgeNewForm(request.POST, project_id=project_id)
        if form.is_valid():
            edge = form.save(commit=False)
            for key in edge.type.keys:
                data[key] = request.POST.get(key, '')
            edge.data = data
            edge.save()

            messages.success(request, 'Edge is added.')
            return redirect('graphs:graphs')
        else:
            messages.error(request, 'Edge new Error')
    else:
        form = ''

    context = {
        'form': form,
        'project_id': project_id
    }

    return render(request, 'graphs/edge_new.html', context)


@login_required
def edge_edit(request):
    pass


def get_keys_from_type(request):
    id = request.GET.get('id', '')
    type = request.GET.get('type', '')
    if type == 'node':
        item = get_object_or_404(NodeType, pk=id)
    else:
        item = get_object_or_404(EdgeType, pk=id)

    data = item.keys

    return HttpResponse(json.dumps(data), content_type='application/json')


@login_required
def project_detail(request, project_id):
    network_nodes = []
    network_edges = []
    project = get_object_or_404(Project, pk=project_id)
    for m in project.modules:
        network_nodes.append({
            'id': m.name,
            'label': m.name
        })

    project_edges = Edge.objects.filter(from_node__module__project=project,
                                        to_node__module__project=project)
    for edge in project_edges:
        if edge.from_node.module != edge.to_node.module:
            network_edges.append({
                'to': edge.to_node.module.name,
                'from': edge.from_node.module.name,
                'label': edge.name
            })

    context = {
        'project': project,
        'network_nodes': json.dumps(network_nodes),
        'network_edges': json.dumps(network_edges)
    }

    return render(request, 'graphs/project_detail.html', context)
