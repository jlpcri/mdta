import json
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from mdta.apps.graphs.utils import node_or_edge_type_edit, node_or_edge_type_new, check_edge_in_set,\
    get_properties_for_node_or_edge, EDGE_TYPES_INVISIBLE_KEY
from mdta.apps.graphs import helpers
from mdta.apps.projects.models import Project, Module
from mdta.apps.projects.utils import context_project_dashboard
from mdta.apps.users.views import user_is_staff, user_is_superuser
from .models import NodeType, EdgeType, Node, Edge
from .forms import NodeTypeNewForm, NodeNewForm, EdgeTypeNewForm, EdgeAutoNewForm
from mdta.apps.projects.forms import ModuleForm, UploadForm
from mdta.apps.testcases.utils import START_NODE_NAME
from mdta.apps.testcases.tasks import create_testcases_celery, push_testcases_to_testrail_celery


@login_required
def home(request):
    user = request.user
    if user.humanresource.project:
        return redirect('graphs:project_detail', user.humanresource.project.id)
    else:
        return redirect('graphs:projects_for_selection')


@login_required
def projects_for_selection(request):
    projects = Project.objects.all()
    context = {
        'projects': projects
    }

    return render(request, 'graphs/projects_for_selection.html', context)


@user_passes_test(user_is_superuser)
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

        context = context_project_dashboard(request)
        context['last_tab'] = 'node_types'

        return render(request, 'projects/project_dashboard.html', context)


@user_passes_test(user_is_staff)
def node_type_edit(request):
    """
    Edit NodeType from apps/graphs
    :param request:
    :return:
    """
    type_id = request.POST.get('editNodeTypeId', '')
    node_type = get_object_or_404(NodeType, pk=type_id)

    if request.method == 'POST':
        node_or_edge_type_edit(request, node_type)

        context = context_project_dashboard(request)
        context['last_tab'] = 'node_types'

        return render(request, 'projects/project_dashboard.html', context)


# @user_passes_test(user_is_staff)
# def project_node_new(request, project_id):
#     """
#     Add new Node from apps/graphs
#     :param request:
#     :param project_id:
#     :return:
#     """
#     if request.method == 'GET':
#         project = get_object_or_404(Project, pk=project_id)
#         form = NodeNewForm(project_id=project_id)
#         context = {
#             'form': form,
#             'project': project
#         }
#
#         return render(request, 'graphs/project/node_new.html', context)
#
#     elif request.method == 'POST':
#         form = NodeNewForm(request.POST, project_id=project_id)
#         if form.is_valid():
#             node = form.save(commit=False)
#
#             properties = get_properties_for_node_or_edge(request, node.type)
#
#             node.properties = properties
#             node.save()
#
#             messages.success(request, 'Node is added.')
#         else:
#             print(form.errors)
#             messages.error(request, 'Node new Error')
#
#         return redirect('graphs:graphs')


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

        context = context_project_dashboard(request)
        context['last_tab'] = 'edge_types'

        return render(request, 'projects/project_dashboard.html', context)


@user_passes_test(user_is_staff)
def edge_type_edit(request):
    """
    Edit EdgeType from apps/graphs
    :param request:
    :return:
    """
    type_id = request.POST.get('editEdgeTypeId', '')
    edge_type = get_object_or_404(EdgeType, pk=type_id)

    if request.method == 'POST':
        node_or_edge_type_edit(request, edge_type)

        context = context_project_dashboard(request)
        context['last_tab'] = 'edge_types'

        return render(request, 'projects/project_dashboard.html', context)


# @user_passes_test(user_is_staff)
# def project_edge_new(request, project_id):
#     """
#     Add new Edge from apps/graphs
#     :param request:
#     :param project_id:
#     :return:
#     """
#     project = get_object_or_404(Project, pk=project_id)
#     if request.method == 'GET':
#         edge_types = EdgeType.objects.order_by('name')
#         edge_priorities = Edge.PRIORITY_CHOICES
#         project_modules = project.module_set.order_by('name')
#         first_module_nodes = project_modules[0].node_set.order_by('name')
#
#         context = {
#             'project': project,
#
#             'edge_types': edge_types,
#             'edge_priorities': edge_priorities,
#             'project_modules': project_modules,
#             'first_module_nodes': first_module_nodes,
#         }
#
#         return render(request, 'graphs/project/edge_new.html', context)
#
#     elif request.method == 'POST':
#         edge_type_id = request.POST.get('project-edge-new-type', '')
#         edge_type = get_object_or_404(EdgeType, pk=edge_type_id)
#
#         properties = get_properties_for_node_or_edge(request, edge_type)
#
#         edge_priority = request.POST.get('project-edge-new-priority', '')
#
#         edge_from_node_id = request.POST.get('project-edge-new-from-node', '')
#         edge_from_node = get_object_or_404(Node, pk=edge_from_node_id)
#
#         edge_to_node_id = request.POST.get('project-edge-new-to-node', '')
#         edge_to_node = get_object_or_404(Node, pk=edge_to_node_id)
#
#         try:
#             edge = Edge.objects.create(
#                 type=edge_type,
#                 priority=edge_priority,
#                 from_node=edge_from_node,
#                 to_node=edge_to_node,
#                 properties=properties
#             )
#             messages.success(request, 'Edge is added.')
#         except (ValueError, ValidationError) as e:
#             messages.error(request, str(e))
#
#         return redirect('graphs:graphs')


def get_keys_from_type(request):
    """
    Fetch keys from NodeType/EdgeType for Node/Edge properties
    :param request:
    :return:
    """
    object_id = request.GET.get('id', '')
    object_type = request.GET.get('type', '')
    if object_type == 'node':
        item = get_object_or_404(NodeType, pk=object_id)
    else:
        item = get_object_or_404(EdgeType, pk=object_id)

    data = {
        'keys': sorted(item.keys),
        'subkeys': item.subkeys
    }

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
    projects = Project.objects.all()
    project = get_object_or_404(Project, pk=project_id)

    user = request.user
    user.humanresource.project = project
    user.humanresource.save()

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

                'type': edge.type.name,
                'to_node': edge.to_node.name,
                'from_node': edge.from_node.name,
                'priority': edge.priority,
                'properties': edge.properties
            })

    # print('**: ', network_edges)

    context = {
        'projects': projects,
        'project': project,
        'module_new_form': ModuleForm(project_id=project.id),
        'module_import_form': UploadForm(),
        'edge_types': EdgeType.objects.all(),
        'edge_priority': Edge.PRIORITY_CHOICES,

        'network_nodes': json.dumps(network_nodes),
        'network_edges': json.dumps(network_edges),

        'edges_between_modules': network_edges
    }

    return render(request, 'graphs/project/project_detail.html', context)


@user_passes_test(user_is_staff)
def project_module_import(request, project_id):
    """
    Add new module from project view
    :param request:
    :param project_id:
    :return:
    """
    if request.method == 'GET':
        form = UploadForm()
        context = {
            'form': form,
            'project_id': project_id
        }
        return render(request, 'graphs/project/module_import.html', context)

    elif request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        # p = get_object_or_404(Project, project_id)
        if form.is_valid():
            if 'file' in request.FILES and request.FILES['file'].name.endswith('.xlsx'):
                result = helpers.upload_vuid(form.cleaned_data['file'], request.user, project_id)
                if result['valid']:
                    messages.success(request, result["message"])
                else:
                    messages.error(request, result['message'])
            elif 'file' in request.FILES:
                messages.error(request, "Invalid file type, unable to upload (must be .xlsx)")
            return redirect('graphs:project_detail', project_id)
        messages.error(request, "Unable to upload file")
        return redirect('graphs:project_detail', project_id)


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
    all_edges = request.GET.get('all_edges', '')

    module = get_object_or_404(Module, pk=module_id)

    # for module level graph
    network_edges = []
    network_nodes = []

    outside_module_node_color = 'rgb(211, 211, 211)'

    for edge in module.edges_all:
        try:
            if edge.properties[EDGE_TYPES_INVISIBLE_KEY] == 'on' and not all_edges:
                continue
        except KeyError:
            pass

        network_edges.append({
            'id': edge.id,
            'to': edge.to_node.id,
            'from': edge.from_node.id
        })

    if request.user.username != 'test':
        for node in module.nodes_all:
            if node.type.name in START_NODE_NAME:
                shape = 'star'
            elif node.type.name in ['DataQueries Database', 'DataQueries WebService']:
                shape = 'ellipse'
            else:
                shape = 'box'

            tmp = {
                'id': node.id,
                'label': node.name,
                'shape': shape
            }
            if node.module != module:
                tmp['color'] = outside_module_node_color

            network_nodes.append(tmp)
    else:
        # try use custom icon for nodes
        image_url = settings.STATIC_URL + 'common/brand_icons/turnpost-png-graphics/'
        for node in module.nodes_all:
            if node.type.name in START_NODE_NAME:
                tmp = {
                    'id': node.id,
                    'label': node.name,
                    'shape': 'star'
                }
            else:
                tmp = {
                    'id': node.id,
                    'label': node.name,
                    'shape': 'image',
                }

                if node.type.name == 'DataQueries Database':
                    tmp['image'] = image_url + 'mdta_database.png'
                elif node.type.name == 'DataQueries WebService':
                    tmp['image'] = image_url + 'mdta_api_web_service.png'
                elif node.type.name == 'Play Prompt':
                    tmp['image'] = image_url + 'mdta_play_prompt.png'
                elif node.type.name == 'Menu Prompt':
                    tmp['image'] = image_url + 'mdta_menu_prompt.png'
                elif node.type.name == 'Menu Prompt with Confirmation':
                    tmp['image'] = image_url + 'mdta_menu_prompt_with_confirm.png'
                elif node.type.name == 'TestHeader End':
                    tmp['image'] = image_url + 'mdta_west_male.png'
                else:
                    tmp['image'] = image_url + 'mdta_west_female.png'

            if node.module != module:
                tmp['shadow'] = 'true'

            network_nodes.append(tmp)

    # print(module.nodes)

    node_form_type_default = get_object_or_404(NodeType, name='Play Prompt')
    node_new_form = NodeNewForm(module_id=module.id, initial={'type': node_form_type_default.id})
    node_types = NodeType.objects.all()
    edge_types = EdgeType.objects.all()
    edge_priorities = Edge.PRIORITY_CHOICES
    current_module_nodes = module.node_set.order_by('name')
    if module.project:
        project_modules = module.project.module_set.order_by('name')
        node_new_node_form = NodeNewForm(project_id=module.project.id,
                                         initial={'type': node_form_type_default.id})
        module_nodes_set = module.project.nodes
    else:
        project_modules = [module]
        node_new_node_form = NodeNewForm(module_id=module.id,
                                         initial={'type': node_form_type_default.id})
        module_nodes_set = current_module_nodes

    module_data_autocomplete = module.data_autocomplete
    data_edge_keys_autocomplete = module_data_autocomplete['data_edge_keys']
    menu_prompt_outputs_keys_autocomplete = module_data_autocomplete['menu_prompt_outputs_keys']
    node_names_autocomplete = module_data_autocomplete['node_names']
    # for node in module_nodes_set:
    #     node_names_autocomplete.append(node.name)

    node_new_edge_form = EdgeAutoNewForm(prefix='edge')

    context = {
        'module': module,
        'all_edges': all_edges,
        'node_new_form': node_new_form,

        'node_types': node_types,
        'edge_types': edge_types,
        'edge_priorities': edge_priorities,
        'project_modules': project_modules,
        'current_module_nodes': current_module_nodes,
        'module_nodes_set': module_nodes_set,
        'node_names_autocomplete': sorted(node_names_autocomplete),
        'data_edge_keys_autocomplete': data_edge_keys_autocomplete,
        'menu_prompt_outputs_keys_autocomplete': menu_prompt_outputs_keys_autocomplete,

        'node_new_node_form': node_new_node_form,
        'node_new_edge_form': node_new_edge_form,

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
    if request.method == 'POST':
        form = NodeNewForm(request.POST)
        if form.is_valid():
            node = form.save(commit=False)

            properties = get_properties_for_node_or_edge(request, node.type)

            node.properties = properties
            node.save()

            messages.success(request, 'Node is Added')
        else:
            # print(form.errors)
            messages.error(request, form.errors)

        return redirect('graphs:project_module_detail', module_id)


@user_passes_test(user_is_staff)
def module_node_new_node_edge(request):
    if request.method == 'POST':
        # print(request.POST)
        from_node_id = request.POST.get('from_node_id', '')
        from_node = get_object_or_404(Node, pk=from_node_id)

        to_node_form = NodeNewForm(request.POST)
        edge_form = EdgeAutoNewForm(request.POST, prefix='edge')
        if to_node_form.is_valid():
            # from_node = node
            to_node = to_node_form.save(commit=False)

            to_node_properties = get_properties_for_node_or_edge(request, to_node.type, auto_edge=True)

            to_node.properties = to_node_properties
            to_node.save()

            edge = edge_form.save(commit=False)
            edge_properties = get_properties_for_node_or_edge(request, edge.type, auto_edge=True)

            try:
                edge.from_node = from_node
                edge.to_node = to_node
                edge.properties = edge_properties
                edge.save()

                messages.success(request, 'Module New Node and Automatic Edge added.')
            except (ValueError, ValidationError) as e:
                to_node.delete()
                messages.error(request, str(e))

        else:
            print(to_node_form.errors)
            messages.error(request, to_node_form.errors)

        return redirect('graphs:project_module_detail', from_node.module.id)


@user_passes_test(user_is_staff)
def module_node_edit(request, node_id):
    """
    Edit node from module view
    :param request:
    :param node_id:
    :return:
    """
    if request.method == 'POST':
        # node_id = request.POST.get('moduleNodeEditId', '')
        node = get_object_or_404(Node, pk=node_id)

        if 'node_save' in request.POST:
            node_name = request.POST.get('moduleNodeEditName', '')
            node_type_id = request.POST.get('moduleNodeEditType', '')
            node_type = get_object_or_404(NodeType, pk=node_type_id)

            properties = get_properties_for_node_or_edge(request, node_type)

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
        edge_type_id = request.POST.get('project-edge-new-type', '')
        edge_type = get_object_or_404(EdgeType, pk=edge_type_id)

        properties = get_properties_for_node_or_edge(request, edge_type)

        edge_priority = request.POST.get('project-edge-new-priority', '')

        edge_from_node_id = request.POST.get('project-edge-new-from-node', '')
        edge_from_node = get_object_or_404(Node, pk=edge_from_node_id)

        edge_to_node_id = request.POST.get('project-edge-new-to-node', '')
        edge_to_node = get_object_or_404(Node, pk=edge_to_node_id)

        try:
            Edge.objects.create(
                type=edge_type,
                priority=edge_priority,
                from_node=edge_from_node,
                to_node=edge_to_node,
                properties=properties
            )
            messages.success(request, 'Edge is added.')
        except (ValueError, ValidationError) as e:
            messages.error(request, str(e))

        return redirect('graphs:project_module_detail', module_id)


@user_passes_test(user_is_staff)
def module_edge_edit(request, edge_id):
    """
    Edit edge from module view
    :param request:
    :param edge_id:
    :return:
    """
    if request.method == 'POST':
        edge = get_object_or_404(Edge, pk=edge_id)

        if 'edge_save' in request.POST:
            module_id = request.POST.get('moduleEdgeEditModuleId', '')

            edge_type_id = request.POST.get('moduleEdgeEditType', '')
            edge_type = get_object_or_404(EdgeType, pk=edge_type_id)

            edge_from = request.POST.get('moduleEdgeEditFromNode', '')
            from_node = get_object_or_404(Node, pk=edge_from)
            edge_to = request.POST.get('moduleEdgeEditToNode', '')
            to_node = get_object_or_404(Node, pk=edge_to)

            edge_priority = request.POST.get('moduleEdgeEditPriority', '')

            properties = get_properties_for_node_or_edge(request, edge_type)

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
            edge_type_id = request.POST.get('projectEdgeEditType', '')
            edge_type = get_object_or_404(EdgeType, pk=edge_type_id)

            edge_from = request.POST.get('projectEdgeEditFromNode', '')
            from_node = get_object_or_404(Node, pk=edge_from)
            edge_to = request.POST.get('projectEdgeEditToNode', '')
            to_node = get_object_or_404(Node, pk=edge_to)

            edge_priority = request.POST.get('projectEdgeEditPriority', '')

            properties = get_properties_for_node_or_edge(request, edge_type)

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


def get_module_id_from_node_id(request):
    node_id = request.GET.get('node_id', '')
    node = get_object_or_404(Node, pk=node_id)

    data = {
        'module_id': node.module.id
    }

    return HttpResponse(json.dumps(data), content_type='application/json')


@user_passes_test(user_is_staff)
def project_publish(request, project_id):
    """
    Project Publish, create testcases and push testcases to TestRail using celery worker
    :param request:
    :param project_id:
    :return:
    """
    project = get_object_or_404(Project, pk=project_id)
    create_testcases_celery.delay(project.id)
    push_testcases_to_testrail_celery.delay(project.id)

    return redirect('testcases:tcs_project')

