import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from mdta.apps.graphs.utils import node_or_edge_type_edit, node_or_edge_type_new, check_edge_in_set

from mdta.apps.projects.models import Project, Module
from mdta.apps.users.views import user_is_staff
from .models import NodeType, EdgeType, Node, Edge
from .forms import NodeTypeNewForm, NodeNewForm, EdgeTypeNewForm, EdgeNewForm, NodeNewNodeForm
from mdta.apps.projects.forms import ModuleForm
from mdta.apps.testcases.utils import START_NODE_NAME


@login_required
def graphs(request):
    """
    View of apps/graphs, include projects list, node type, edge type
    :param request:
    :return:
    """
    context = {
        'projects': Project.objects.all(),
        'test_headers': Module.objects.filter(project=None),

        'node_types': NodeType.objects.all(),
        'edge_types': EdgeType.objects.all(),

        'node_type_new_form': NodeTypeNewForm(),
        'edge_type_new_form': EdgeTypeNewForm(),
    }
    return render(request, 'graphs/graphs.html', context)


@user_passes_test(user_is_staff)
def node_type_new(request):
    """
    Add new NodeType from apps/graphs
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = NodeTypeNewForm(request.POST)
        node_or_edge_type_new(request, form)

        return redirect('graphs:graphs')


@user_passes_test(user_is_staff)
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


@user_passes_test(user_is_staff)
def project_node_new(request, project_id):
    """
    Add new Node from apps/graphs
    :param request:
    :param project_id:
    :return:
    """
    if request.method == 'GET':
        project = get_object_or_404(Project, pk=project_id)
        form = NodeNewForm(project_id=project_id)
        context = {
            'form': form,
            'project': project
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

        return redirect('graphs:graphs')


@user_passes_test(user_is_staff)
def edge_type_new(request):
    """
    Add new EdgeType from apps/graphs
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = EdgeTypeNewForm(request.POST)
        node_or_edge_type_new(request, form)

        return redirect('graphs:graphs')


@user_passes_test(user_is_staff)
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


@user_passes_test(user_is_staff)
def project_edge_new(request, project_id):
    """
    Add new Edge from apps/graphs
    :param request:
    :param project_id:
    :return:
    """
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'GET':
        edge_types = EdgeType.objects.order_by('name')
        edge_priorities = Edge.PRIORITY_CHOICES
        project_modules = project.module_set.order_by('name')
        first_module_nodes = project_modules[0].node_set.order_by('name')

        context = {
            'project': project,

            'edge_types': edge_types,
            'edge_priorities': edge_priorities,
            'project_modules': project_modules,
            'first_module_nodes': first_module_nodes,
        }

        return render(request, 'graphs/project/edge_new.html', context)

    elif request.method == 'POST':
        properties = {}
        edge_type_id = request.POST.get('project-edge-new-type', '')
        edge_type = get_object_or_404(EdgeType, pk=edge_type_id)
        for key in edge_type.keys:
            properties[key] = request.POST.get(key, '')

        edge_priority = request.POST.get('project-edge-new-priority', '')

        edge_from_node_id = request.POST.get('project-edge-new-from-node', '')
        edge_from_node = get_object_or_404(Node, pk=edge_from_node_id)

        edge_to_node_id = request.POST.get('project-edge-new-to-node', '')
        edge_to_node = get_object_or_404(Node, pk=edge_to_node_id)

        try:
            edge = Edge.objects.create(
                type=edge_type,
                priority=edge_priority,
                from_node=edge_from_node,
                to_node=edge_to_node,
                properties=properties
            )
            messages.success(request, 'Edge is added.')
        except (ValueError, ValidationError) as e:
            messages.error(request, str(e))

        return redirect('graphs:graphs')


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
        if not check_edge_in_set(edge, network_edges):
            network_edges.append({
                'id': edge.id,
                'to': edge.to_node.module.id,
                'from': edge.from_node.module.id,
                'label': 1,
                'edge_name': edge.from_node.name + '-' + edge.to_node.name,

                'type': edge.type.id,
                'to_node': edge.to_node.id,
                'from_node': edge.from_node.id,
                'priority': edge.priority,
                'properties': edge.properties
            })

    # print('**: ', network_edges)

    context = {
        'project': project,
        'module_new_form': ModuleForm(project_id=project.id),
        'edge_types': EdgeType.objects.all(),
        'edge_priority': Edge.PRIORITY_CHOICES,

        'network_nodes': json.dumps(network_nodes),
        'network_edges': json.dumps(network_edges),

        'edges_between_modules': network_edges
    }

    return render(request, 'graphs/project/project_detail.html', context)


@user_passes_test(user_is_staff)
def project_module_new(request, project_id):
    """
    Add new module from project view
    :param request:
    :param project_id:
    :return:
    """
    if request.method == 'GET':
        form = ModuleForm(project_id=project_id)
        context = {
            'form': form,
            'project_id': project_id
        }
        return render(request, 'graphs/project/module_new.html', context)
    elif request.method == 'POST':
        form = ModuleForm(request.POST)
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

    # for module level graph
    network_edges = []
    network_nodes = []

    outside_module_node_color = 'rgb(211, 211, 211)'
    start_node_shape = 'star'
    normal_node_shape = 'box'

    for edge in module.edges_all:
        network_edges.append({
            'id': edge.id,
            'to': edge.to_node.id,
            'from': edge.from_node.id
        })

    for node in module.nodes_all:
        if node.module != module:
            network_nodes.append({
                'id': node.id,
                'label': node.name,
                'color': outside_module_node_color,
                'shape': start_node_shape if node.type.name == START_NODE_NAME else normal_node_shape
            })
        else:
            network_nodes.append({
                'id': node.id,
                'label': node.name,
                'shape': start_node_shape if node.type.name == START_NODE_NAME else normal_node_shape
            })

    # print(module.nodes)

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


@user_passes_test(user_is_staff)
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
            except (ValueError, ValidationError) as e:
                messages.error(request, str(e))

        if 'module_delete' in request.POST:
            module.delete()
            messages.success(request, 'Module is deleted.')

        return redirect('graphs:project_detail', project_id)


@user_passes_test(user_is_staff)
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
            # print(request.POST)
            # return redirect('graphs:project_module_detail', module_id)
            node_form = NodeNewForm(request.POST)
            edge_type_id = request.POST.get('moduleNodeEdgeNewEdgeType', '')
            edge_priority = request.POST.get('moduleNodeEdgeNewEdgePriority', '')
            from_node_id = request.POST.get('moduleNodeEdgeNewFromNodeId', '')
            if node_form.is_valid():
                from_node = get_object_or_404(Node, pk=from_node_id)
                to_node = node_form.save(commit=False)
                node_properties = {}
                for key in to_node.type.keys:
                    node_properties[key] = request.POST.get('node_' + key, '')
                to_node.properties = node_properties
                to_node.save()

                edge_properties = {}
                edge_type = get_object_or_404(EdgeType, pk=edge_type_id)
                for key in edge_type.keys:
                    edge_properties[key] = request.POST.get('edge_' + key, '')
                try:
                    edge = Edge.objects.create(
                        type=edge_type,
                        priority=edge_priority,
                        from_node=from_node,
                        to_node=to_node,
                        properties=edge_properties,
                    )
                    messages.success(request, 'Module New Node and Automatic Edge added.')
                except (ValueError, ValidationError) as e:
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


@user_passes_test(user_is_staff)
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
            except (ValueError, ValidationError) as e:
                messages.error(request, str(e))

        if 'node_delete' in request.POST:
            node.delete()
            messages.success(request, 'Node is deleted.')

        return redirect('graphs:project_module_detail', node.module.id)


@user_passes_test(user_is_staff)
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


@user_passes_test(user_is_staff)
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
            module_id = request.POST.get('moduleEdgeEditModuleId', '')

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
                edge.type = edge_type
                edge.from_node = from_node
                edge.to_node = to_node
                edge.priority = edge_priority
                edge.properties = properties
                edge.save()
                # messages.success(request, 'Edge is saved.')
            except (ValueError, ValidationError) as e:
                messages.error(request, str(e))

            return redirect('graphs:project_module_detail', module_id)

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
            except (ValueError, ValidationError) as e:
                messages.error(request, str(e))

            return redirect('graphs:project_detail', edge.from_node.module.project.id)
        elif 'project_edge_delete' in request.POST:
            edge.delete()
            return redirect('graphs:project_detail', edge.from_node.module.project.id)


def get_nodes_from_module(request):
    """
    Get nodes of module, for add new Edge of project level
    to select nodes from different module
    :param request:
    :return:
    """
    module_id = request.GET.get('module_id', '')
    module = get_object_or_404(Module, pk=module_id)
    data = []

    for item in module.node_set.order_by('name'):
        data.append({
            'id': item.id,
            'name': item.name
        })

    return HttpResponse(json.dumps(data), content_type='application/json')

