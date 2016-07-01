import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from mdta.apps.graphs.utils import node_or_edge_type_edit, node_or_edit_type_new

from mdta.apps.projects.models import Project, Module
from .models import NodeType, EdgeType, Node, Edge
from .forms import NodeTypeNewForm, NodeNewForm, EdgeTypeNewForm, EdgeNewForm, NodeNewNodeForm
from mdta.apps.projects.forms import ModuleNewForm


@login_required
def graphs(request):
    """
    View of apps/graphs, include projects list, node type, edge type
    :param request:
    :return:
    """
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
    """
    Add new NodeType from apps/graphs
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = NodeTypeNewForm(request.POST)
        node_or_edit_type_new(request, form)

        return redirect('graphs:graphs')


@login_required
def node_type_edit(request):
    """
    Edit NodeType from apps/graphs
    :param request:
    :return:
    """
    id = request.POST.get('editNodeTypeId', '')
    node_type = get_object_or_404(NodeType, pk=id)

    if request.method == 'POST':
        node_or_edge_type_edit(request, node_type)

        return redirect('graphs:graphs')


@login_required
def project_node_new(request, project_id):
    """
    Add new Node from apps/graphs
    :param request:
    :param project_id:
    :return:
    """
    if request.method == 'GET':
        form = NodeNewForm(project_id=project_id)
        context = {
            'form': form,
            'project_id': project_id
        }

        return render(request, 'graphs/project/node_new.html', context)

    elif request.method == 'POST':
        properties = {}
        form = NodeNewForm(request.POST, project_id=project_id)
        if form.is_valid():
            node = form.save(commit=False)
            for key in node.type.keys:
                properties[key] = request.POST.get(key, '')
            node.properties = properties
            node.save()

            messages.success(request, 'Node is added.')
        else:
            print(form.errors)
            messages.error(request, 'Node new Error')

        return redirect('graphs:project_detail', project_id)


@login_required
def edge_type_new(request):
    """
    Add new EdgeType from apps/graphs
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = EdgeTypeNewForm(request.POST)
        node_or_edit_type_new(request, form)

        return redirect('graphs:graphs')


@login_required
def edge_type_edit(request):
    """
    Edit EdgeType from apps/graphs
    :param request:
    :return:
    """
    id = request.POST.get('editEdgeTypeId', '')
    edge_type = get_object_or_404(EdgeType, pk=id)

    if request.method == 'POST':
        node_or_edge_type_edit(request, edge_type)

        return redirect('graphs:graphs')


@login_required
def project_edge_new(request, project_id):
    """
    Add new Edge from apps/graphs
    :param request:
    :param project_id:
    :return:
    """
    if request.method == 'GET':
        form = EdgeNewForm(project_id=project_id)
        context = {
            'form': form,
            'project_id': project_id
        }

        return render(request, 'graphs/project/edge_new.html', context)

    elif request.method == 'POST':
        properties = {}
        form = EdgeNewForm(request.POST, project_id=project_id)
        if form.is_valid():
            edge = form.save(commit=False)
            for key in edge.type.keys:
                properties[key] = request.POST.get(key, '')
            edge.properties = properties
            edge.save()
            messages.success(request, 'Edge is added.')
        else:
            messages.error(request, 'Edge new Error')

        return redirect('graphs:project_detail', project_id)


def get_keys_from_type(request):
    """
    Fetch keys from NodeType/EdgeType for Node/Edge properties
    :param request:
    :return:
    """
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
    """
    Project detail, include graphical representation: modules in this project
    :param request:
    :param project_id:
    :return:
    """
    network_nodes = []
    network_edges = []
    project = get_object_or_404(Project, pk=project_id)
    for m in project.modules:
        network_nodes.append({
            'id': m.id,
            'label': m.name
        })

    for edge in project.edges_between_modules:
        network_edges.append({
            'id': edge.id,
            'to': edge.to_node.module.id,
            'from': edge.from_node.module.id,
            # 'label': edge.name
        })

    # Remove duplicate edge between two modules
    # network_edges = [dict(t) for t in set([tuple(d.items()) for d in network_edges])]

    context = {
        'project': project,
        'module_new_form': ModuleNewForm(project_id=project.id),
        'edge_types': EdgeType.objects.all(),
        'edge_priority': Edge.PRIORITY_CHOICES,

        'network_nodes': json.dumps(network_nodes),
        'network_edges': json.dumps(network_edges)
    }

    return render(request, 'graphs/project/project_detail.html', context)


@login_required
def project_module_new(request, project_id):
    """
    Add new module from project view
    :param request:
    :param project_id:
    :return:
    """
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
def project_module_detail(request, module_id):
    """
    Module detail from project view, include graphical representation of Nodes in this module
    :param request:
    :param module_id:
    :return:
    """
    module = get_object_or_404(Module, pk=module_id)
    network_nodes = []
    network_edges = []

    for n in module.nodes:
        network_nodes.append({
            'id': n.id,
            'label': n.name
        })

    module_edges = Edge.objects.filter(from_node__module=module,
                                       to_node__module=module)
    for edge in module_edges:
        network_edges.append({
            'id': edge.id,
            'to': edge.to_node.id,
            'from': edge.from_node.id
        })

    context = {
        'module': module,
        'node_new_form': NodeNewForm(module_id=module_id),
        'edge_new_form': EdgeNewForm(module_id=module_id),
        'node_new_node_form': NodeNewNodeForm(module_id=module_id),
        'node_types': NodeType.objects.all(),
        'edge_types': EdgeType.objects.all(),

        'edge_priority': Edge.PRIORITY_CHOICES,

        'network_nodes': json.dumps(network_nodes),
        'network_edges': json.dumps(network_edges)
    }

    return render(request, 'graphs/module/module_detail.html', context)


@login_required
def project_module_edit(request, project_id):
    """
    Edit module from project view, include Edition/Deletion
    :param request:
    :param project_id:
    :return:
    """
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
def module_node_new(request, module_id):
    """
    Add new node from module view
    :param request:
    :param module_id:
    :return:
    """
    auto_edge = request.GET.get('auto_edge', '')
    if request.method == 'POST':
        if auto_edge == 'node_edge_new':
            node_form = NodeNewForm(request.POST)
            edge_type_id = request.POST.get('moduleNodeEdgeNewEdgeType', '')
            edge_priority = request.POST.get('moduleNodeEdgeNewEdgePriority', '')
            from_node_id = request.POST.get('moduleNodeEdgeNewFromNodeId', '')
            if node_form.is_valid():
                from_node = get_object_or_404(Node, pk=from_node_id)
                to_node = node_form.save()
                edge_properties = {}

                edge_type = get_object_or_404(EdgeType, pk=edge_type_id)
                for key in edge_type.keys:
                    edge_properties[key] = request.POST.get(key, '')
                try:
                    edge = Edge.objects.create(
                        type=edge_type,
                        priority=edge_priority,
                        from_node=from_node,
                        to_node=to_node,
                        properties=edge_properties,
                    )
                    messages.success(request, 'Module New Node and Automatic Edge added.')
                except Exception as e:
                    to_node.delete()
                    messages.error(request, str(e))

            else:
                print(node_form.errors)
                messages.error(request, node_form.errors)

        else:
            properties = {}
            form = NodeNewForm(request.POST)
            if form.is_valid():
                node = form.save(commit=False)
                for key in node.type.keys:
                    properties[key] = request.POST.get(key, '')
                node.properties = properties
                node.save()

                messages.success(request, 'Node is Added')
            else:
                print(form.errors)
                messages.error(request, 'Module new node error.')

        return redirect('graphs:project_module_detail', module_id)


@login_required
def module_node_edit(request, node_id):
    """
    Edit node from module view
    :param request:
    :param module_id:
    :return:
    """
    if request.method == 'POST':
        # node_id = request.POST.get('moduleNodeEditId', '')
        node = get_object_or_404(Node, pk=node_id)

        if 'node_save' in request.POST:
            properties = {}
            node_name = request.POST.get('moduleNodeEditName', '')
            node_type_id = request.POST.get('moduleNodeEditType', '')
            node_type = get_object_or_404(NodeType, pk=node_type_id)
            for key in node_type.keys:
                properties[key] = request.POST.get(key, '')

            try:
                node.name = node_name
                node.type = node_type
                node.properties = properties
                node.save()
                # messages.success(request, 'Node is saved.')
            except Exception as e:
                messages.error(request, str(e))

        if 'node_delete' in request.POST:
            node.delete()
            messages.success(request, 'Node is deleted.')

        return redirect('graphs:project_module_detail', node.module.id)


@login_required
def module_edge_new(request, module_id):
    """
    Add new edge from module view
    :param request:
    :param module_id:
    :return:
    """
    if request.method == 'POST':
        properties = {}
        form = EdgeNewForm(request.POST)
        if form.is_valid():
            edge = form.save(commit=False)
            for key in edge.type.keys:
                properties[key] = request.POST.get(key, '')

            edge.properties = properties
            edge.save()
            messages.success(request, 'Edge is added.')
        else:
            print(form.errors)
            messages.error(request, 'Module new edge error.')

        return redirect('graphs:project_module_detail', module_id)


@login_required
def module_edge_edit(request, edge_id):
    """
    Edit edge from module view
    :param request:
    :param module_id:
    :return:
    """
    if request.method == 'POST':
        edge = get_object_or_404(Edge, pk=edge_id)

        if 'edge_save' in request.POST:
            properties = {}
            # edge_name = request.POST.get('moduleEdgeEditName', '')

            edge_type_id = request.POST.get('moduleEdgeEditType', '')
            edge_type = get_object_or_404(EdgeType, pk=edge_type_id)

            edge_from = request.POST.get('moduleEdgeEditFromNode', '')
            from_node = get_object_or_404(Node, pk=edge_from)
            edge_to = request.POST.get('moduleEdgeEditToNode', '')
            to_node = get_object_or_404(Node, pk=edge_to)

            edge_priority = request.POST.get('moduleEdgeEditPriority', '')

            for key in edge_type.keys:
                properties[key] = request.POST.get(key, '')

            try:
                # edge.name = edge_name
                edge.type = edge_type
                edge.from_node = from_node
                edge.to_node = to_node
                edge.priority = edge_priority
                edge.properties = properties
                edge.save()
                # messages.success(request, 'Edge is saved.')
            except Exception as e:
                messages.error(request, str(e))

            return redirect('graphs:project_module_detail', edge.from_node.module.id)

        elif 'edge_delete' in request.POST:
            edge.delete()
            messages.success(request, 'Edge is deleted.')
            return redirect('graphs:project_module_detail', edge.from_node.module.id)

        elif 'project_edge_save' in request.POST:
            properties = {}
            edge_type_id = request.POST.get('projectEdgeEditType', '')
            edge_type = get_object_or_404(EdgeType, pk=edge_type_id)

            edge_from = request.POST.get('projectEdgeEditFromNode', '')
            from_node = get_object_or_404(Node, pk=edge_from)
            edge_to = request.POST.get('projectEdgeEditToNode', '')
            to_node = get_object_or_404(Node, pk=edge_to)

            edge_priority = request.POST.get('projectEdgeEditPriority', '')

            for key in edge_type.keys:
                properties[key] = request.POST.get(key, '')

            try:
                edge.type = edge_type
                edge.from_node = from_node
                edge.to_node = to_node
                edge.priority = edge_priority
                edge.properties = properties
                edge.save()
            except Exception as e:
                messages.error(request, str(e))

            return redirect('graphs:project_detail', edge.from_node.module.project.id)
        elif 'project_edge_delete' in request.POST:
            edge.delete()
            return redirect('graphs:project_detail', edge.from_node.module.project.id)




