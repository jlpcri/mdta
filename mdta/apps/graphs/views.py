import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from mdta.apps.graphs.utils import node_or_edge_type_edit, node_or_edit_type_new

from mdta.apps.projects.models import Project, Module
from .models import NodeType, EdgeType, Edge
from .forms import NodeTypeNewForm, NodeNewForm, EdgeTypeNewForm, EdgeNewForm
from mdta.apps.projects.forms import ModuleNewForm


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
def project_new_node(request, project_id):
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

    return render(request, 'graphs/project/node_new.html', context)


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
def project_new_edge(request, project_id):
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

    return render(request, 'graphs/project/edge_new.html', context)


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
                # 'label': edge.name
            })

    # Remove duplicate edge between two modules
    network_edges = [dict(t) for t in set([tuple(d.items()) for d in network_edges])]

    context = {
        'project': project,
        'module_new_form': ModuleNewForm(project_id=project.id),

        'network_nodes': json.dumps(network_nodes),
        'network_edges': json.dumps(network_edges)
    }

    return render(request, 'graphs/project/project_detail.html', context)


@login_required
def module_new(request, project_id):
    if request.method == 'POST':
        form = ModuleNewForm(request.POST)
        if form.is_valid():
            module = form.save()
            messages.success(request, 'Module \'{0}\' is added to \'{1}\''.format(module.name, module.project.name))
        else:
            print(form.errors)
            messages.error(request, 'Errors found.')

        return redirect('graphs:project_detail', project_id)


@login_required
def module_detail(request, module_id):
    module = get_object_or_404(Module, pk=module_id)
    network_nodes = []
    network_edges = []

    for n in module.nodes:
        network_nodes.append({
            'id': n.name,
            'label': n.name
        })

    module_edges = Edge.objects.filter(from_node__module=module,
                                       to_node__module=module)
    for edge in module_edges:
        network_edges.append({
            'to': edge.to_node.name,
            'from': edge.from_node.name
        })

    context = {
        'module': module,
        'node_new_form': NodeNewForm(module_id=module_id),
        'edge_new_form': EdgeNewForm(module_id=module_id),

        'network_nodes': json.dumps(network_nodes),
        'network_edges': json.dumps(network_edges)
    }

    return render(request, 'graphs/module/module_detail.html', context)


@login_required
def module_edit(request, project_id):
    if request.method == 'POST':
        module_id = request.POST.get('editModuleId', '')
        module = get_object_or_404(Module, pk=module_id)

        if 'module_save' in request.POST:
            module_name = request.POST.get('editModuleName', '')

            try:
                module.name = module_name
                module.save()
                messages.success(request, 'Module is saved.')
            except Exception as e:
                messages.error(request, str(e))

        if 'module_delete' in request.POST:
            module.delete()
            messages.success(request, 'Module is deleted.')

        return redirect('graphs:project_detail', project_id)


@login_required
def module_new_node(request, module_id):
    pass


@login_required
def module_edit_node(request, module_id):
    pass
