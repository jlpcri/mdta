import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ValidationError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from mdta.apps.graphs.utils import node_or_edge_type_edit, node_or_edge_type_new, check_edge_in_set,\
    get_properties_for_node_or_edge, node_related_edges_invisible, self_reference_edge_node_in_set,\
    get_positions_for_node
from mdta.apps.projects.models import Project, Module, Language
from mdta.apps.graphs import helpers
from mdta.apps.projects.utils import context_project_dashboard
from mdta.apps.users.views import user_is_staff, user_is_superuser
from .models import NodeType, EdgeType, Node, Edge
from .forms import NodeTypeNewForm, NodeNewForm, EdgeTypeNewForm, EdgeAutoNewForm
from mdta.apps.projects.forms import ModuleForm, UploadForm, LanguageNewForm
from mdta.apps.testcases.constant_names import *
from mdta.apps.testcases.tasks import create_testcases_celery
from mdta.apps.testcases.models import TestCaseResults


@login_required
def home(request):
    user = request.user
    if user.humanresource.project:
        return redirect('graphs:project_detail', user.humanresource.project.id)
    else:
        return redirect('graphs:projects_for_selection')


@login_required
def projects_for_selection(request):
    tmp1 = []
    tmp2 = []

    ps = Project.objects.filter(archive=False)
    for idx, p in enumerate(ps):
        if idx % 2 == 0:
            tmp1.append(p)
        else:
            tmp2.append(p)

    if len(tmp1) > len(tmp2):
        tmp2.append('')
    elif len(tmp1) < len(tmp2):
        tmp1.append('')

    projects = list(zip(tmp1, tmp2))
    # for p in projects:
    #     print(p)
    context = {
        'projects': projects
    }

    return render(request, 'graphs/projects_for_selection.html', context)


@user_passes_test(user_is_staff)
def graphs(request):
    """
    View of apps/graphs, include projects list, node type, edge type
    :param request:
    :return:
    """
    context = {
        'projects': Project.objects.filter(archive=False),
        'test_headers': Module.objects.filter(project=None),

        'node_types': NodeType.objects.all(),
        'edge_types': EdgeType.objects.all(),

        'node_type_new_form': NodeTypeNewForm(),
        'edge_type_new_form': EdgeTypeNewForm(),
    }
    return render(request, 'graphs/graphs.html', context)


@user_passes_test(user_is_superuser)
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


@user_passes_test(user_is_superuser)
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


@user_passes_test(user_is_superuser)
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


@user_passes_test(user_is_superuser)
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
        data = {
            'keys': sorted(item.keys),
            'subkeys': item.subkeys,
            'v_keys': item.verbiage_keys
        }
    else:
        item = get_object_or_404(EdgeType, pk=object_id)
        data = {
            'keys': sorted(item.keys),
            'subkeys': item.subkeys,
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
    all_edges = request.GET.get('all_edges', '')
    draw_invisible_button = ''

    network_nodes = []
    network_edges = []
    tc_keys = []
    # projects = Project.objects.filter(archive=False)
    project = get_object_or_404(Project, pk=project_id)
    try:
        tests = project.testcaseresults_set.latest('updated').results
        testcase = TestCaseResults.objects.filter(project=project)
    except TestCaseResults.DoesNotExist:
        tests = []

    user = request.user
    if user.humanresource.project != project:
        user.humanresource.project = project
        user.humanresource.save()

    for tc in tests:
        data = tc['data']
        tc_keys.append(data)

    for m in project.modules:
        try:
            positions = m.properties[NODE_POSITIONS_KEY]
        except TypeError:
            positions = None
        network_nodes.append({
            'id': m.id,
            'label': m.name,
            'positions': positions,
            'start_module': m.start_module
        })
    for d, n in zip(network_nodes, tc_keys):
        d['data'] = n
    # print(tests)
    for edge in project.edges_between_modules:
        try:
            if edge.properties[EDGE_TYPES_INVISIBLE_KEY] == 'on':
                draw_invisible_button = 'true'
                if not all_edges:
                    continue
        except KeyError:
            pass

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

    context = {
        # 'projects': projects,
        'project': project,
        'all_edges': all_edges,
        'draw_invisible_button': draw_invisible_button,

        'module_new_form': ModuleForm(project_id=project.id),
        'module_import_form': UploadForm(),
        'language_new_form': LanguageNewForm(initial={'project': project}),

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
        # form = UploadForm()
        # context = {
        #     'form': form,
        #     'project_id': project_id
        # }
        # return render(request, 'graphs/project/module_import.html', context)
        # messages.error(request, "Unable to upload file")
        return redirect('graphs:project_detail', project_id)

    elif request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
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
        module_position = json.loads(request.POST.get('positions'))
        if form.is_valid():
            module = form.save(commit=False)
            module.properties = {
                NODE_POSITIONS_KEY: {
                    NODE_X_KEY: module_position[NODE_X_KEY],
                    NODE_Y_KEY: module_position[NODE_Y_KEY]
                }
            }
            module.save()
            messages.success(request, 'Module \'{0}\' is added to \'{1}\''.format(module.name, module.project.name))
        else:
            print(form.errors)
            messages.error(request, form.errors)

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
    draw_invisible_button = ''

    module = get_object_or_404(Module, pk=module_id)

    # for module level graph
    network_edges = []
    network_nodes = []
    tc_keys = []
    data_keys = []
    edge_id = []
    merged = {}
    edge_reference_sizes = []

    inside_module_node_color = 'rgb(128, 191, 255)'
    outside_module_node_color = 'rgb(211, 211, 211)'

    for edge in module.edges_all:
        try:
            if edge.properties[EDGE_TYPES_INVISIBLE_KEY] == 'on':
                draw_invisible_button = 'true'
                if not all_edges:
                    continue
        except KeyError:
            pass

        self_reference_size = 20
        if edge.from_node.id == edge.to_node.id:
            self_reference_data = self_reference_edge_node_in_set(edge, network_edges, edge_reference_sizes)
            if self_reference_data['flag']:
                self_reference_size = self_reference_data['size']

        network_edges.append({
            'id': edge.id,
            'to': edge.to_node.id,
            'from': edge.from_node.id,
            'name': edge.from_node.name + ' - ' + edge.to_node.name,
            'selfReferenceSize': self_reference_size
        })

    try:
        tmp_data = module.project.testcaseresults_set.latest('updated').results
        try:
            tests = [(item for item in tmp_data if item['module'] == module.name).__next__()]
            for tc in tests:
                data = tc['data']
                tc_keys.append(data)
            for tc in tc_keys:
                data = tc
            for d in data:
                data_keys.append(d)
            for item in data_keys:
                e_id = item['id']
                if 'tcs_cannot_route' in item:
                    if 'gap_color' in item:
                        continue
                    tcr = item['tcs_cannot_route']
                    edge_id.append({'id': e_id,
                                    'tcs_cannot_route': tcr})
            for item in network_edges + edge_id:
                if item['id'] in merged:
                    merged[item['id']].update(item)
                else:
                    merged[item['id']] = item
        except StopIteration:
            pass
    except (AttributeError, TestCaseResults.DoesNotExist):
        tmp_data = []
        tests = []

    # print(network_edges)

    for node in module.nodes_all:
        image = NODE_IMAGE[node.type.name]

        # get node position in current module
        try:
            positions = node.properties[NODE_POSITIONS_KEY][module_id]
        except KeyError:
            positions = None
        tmp = {
            'id': node.id,
            'module_id': node.module.id,
            'label': node.name,
            'image': image,
            'color': inside_module_node_color,
            'positions': positions
        }
        if node.module != module:
            if node_related_edges_invisible(node, module) and not all_edges:
                continue
            tmp['color'] = outside_module_node_color

        network_nodes.append(tmp)

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
        'draw_invisible_button': draw_invisible_button,
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
            except (ValueError, ValidationError) as e:
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
    if request.method == 'POST':
        form = NodeNewForm(request.POST)
        node_position = json.loads(request.POST.get('positions'))

        if form.is_valid():
            node = form.save(commit=False)

            properties = get_properties_for_node_or_edge(request, node.type)

            # set initial position of new node
            properties[NODE_POSITIONS_KEY] = {
                module_id: {
                    NODE_X_KEY: node_position[NODE_X_KEY],
                    NODE_Y_KEY: node_position[NODE_Y_KEY]
                }
            }

            node.properties = properties
            node.save()

            # messages.success(request, 'Node is Added')
        else:
            # print(form.errors)
            messages.error(request, form.errors)

        return redirect('graphs:project_module_detail', module_id)


@login_required
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

            # set initial position of new node
            to_node_properties[NODE_POSITIONS_KEY] = {
                from_node.module.id: {
                    NODE_X_KEY: NODE_X_INITIAL,
                    NODE_Y_KEY: NODE_Y_INITIAL
                }
            }

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


@login_required
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

            properties[NODE_POSITIONS_KEY] = get_positions_for_node(request, node)

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
            # messages.success(request, 'Node is deleted.')

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
            # messages.success(request, 'Edge is added.')
        except (ValueError, ValidationError) as e:
            messages.error(request, str(e))

        return redirect('graphs:project_module_detail', module_id)


@login_required
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
            # messages.success(request, 'Edge is deleted.')
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
    if node.module.project:  # node in Project.modules
        if node.module.project.language:
            language = {
                'name': node.module.project.language.name,
                'id': node.module.project.language.id
            }
        else:
            language = {
                'name': '',
                'id': ''
            }

        project_languages = Language.objects.filter(project=node.module.project)
        languages = []
        if project_languages.count() > 0:
            for item in project_languages:
                languages.append({
                    'name': item.name,
                    'id': item.id
                })
        else:
            languages.append({
                'name': LANGUAGE_DEFAULT_NAME,
                'id': -1
            })

        node_in = 'module'
    else:  # node in test header
        projects = Project.objects.filter(test_header=node.module)
        projects_languages = []
        languages = []
        for project in projects:
            projects_languages += Language.objects.filter(project=project)
        if len(projects_languages) > 0:
            for item in projects_languages:
                tmp = any(lan['name'] == item.name for lan in languages)
                if not tmp:
                    languages.append({
                        'name': item.name,
                        'id': item.id
                    })
        else:
            languages.append({
                'name': LANGUAGE_DEFAULT_NAME,
                'id': -1
            })
        language = {
                'name': '',
                'id': ''
            }

        node_in = 'testheader'

    node_data = {
        'name': node.name,
        'type_id': node.type.id,
        'type_name': node.type.name,
        'properties': node.properties,
        'verbiage': node.verbiage,
        'node_keys': node.type.keys,
        'v_keys': node.type.verbiage_keys,
        'language': language,  # language default value of node
        'languages': languages,  # all possible languages of current node of module of project
        'node_in': node_in,  # determine node whether in test header or not
    }

    data = {
        'module_id': node.module.id,
        'node_data': node_data
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

    # return redirect('testcases:tcs_project')
    return HttpResponse(json.dumps(project.id), content_type="application/json")


def module_node_verbiage_edit(request):
    """
    Edit Node data modal
    :param request:
    :return:
    """
    if request.method == 'POST':
        node_id = request.POST.get('moduleNodeEditId', '')
        node = get_object_or_404(Node, pk=node_id)

        if 'node_save' in request.POST:
            node_name = request.POST.get('moduleNodeEditName', '')
            node_type_id = request.POST.get('moduleNodeEditType', '')
            node_type = get_object_or_404(NodeType, pk=node_type_id)

            properties = get_properties_for_node_or_edge(request, node_type)
            properties[NODE_POSITIONS_KEY] = get_positions_for_node(request, node)
            # print(request.POST)

            language_name = ''
            language_list = request.POST.getlist('moduleNodeEditVerbiageLanguage', '')
            if language_list:
                language_id = language_list[0]
                if int(language_id) > 0:
                    language = get_object_or_404(Language, pk=language_id)
                    language_name = language.name
                else:
                    language_name = LANGUAGE_DEFAULT_NAME

            verbiage = {}
            for key in node_type.verbiage_keys:
                verbiage[key] = request.POST.get(key, '')

            try:
                node.name = node_name
                node.type = node_type
                node.properties = properties
                if language_name:
                    if node.verbiage:
                        node.verbiage[language_name] = verbiage
                    else:
                        node.verbiage = {
                            language_name: verbiage
                        }
                else:
                    node.verbiage = {}
                node.save()
            except (ValueError, ValidationError) as e:
                messages.error(request, str(e))

        elif 'node_delete' in request.POST:
            node.delete()
            messages.success(request, 'Node is deleted.')

        return redirect('graphs:project_module_detail', node.module.id)


def node_save_positions(request):
    save_type = request.GET.get('type', '')
    positions = json.loads(request.POST.get('positions'))
    if request.method == 'POST':
        if save_type == 'module':
            for item in positions:
                module = get_object_or_404(Module, pk=item['module_id'])
                try:
                    module.properties[NODE_POSITIONS_KEY][NODE_X_KEY] = item[NODE_X_KEY]
                    module.properties[NODE_POSITIONS_KEY][NODE_Y_KEY] = item[NODE_Y_KEY]
                except TypeError:
                    module.properties = {
                        NODE_POSITIONS_KEY: {
                            NODE_X_KEY: item[NODE_X_KEY],
                            NODE_Y_KEY: item[NODE_Y_KEY]
                        }
                    }

                module.save()
        else:
            module_id = request.POST.get('module_id')
            # print(module_id)
            for item in positions:
                # print(item['node_id'], item['posx'], item['posy'])
                node = get_object_or_404(Node, pk=item['node_id'])

                if NODE_POSITIONS_KEY in node.properties:
                    if module_id in node.properties[NODE_POSITIONS_KEY]:
                        node.properties[NODE_POSITIONS_KEY][module_id][NODE_X_KEY] = item[NODE_X_KEY]
                        node.properties[NODE_POSITIONS_KEY][module_id][NODE_Y_KEY] = item[NODE_Y_KEY]
                    else:
                        node.properties[NODE_POSITIONS_KEY][module_id] = {
                            NODE_X_KEY: item[NODE_X_KEY],
                            NODE_Y_KEY: item[NODE_Y_KEY]
                        }
                else:
                    node.properties[NODE_POSITIONS_KEY] = {
                        module_id: {
                            NODE_X_KEY: item[NODE_X_KEY],
                            NODE_Y_KEY: item[NODE_Y_KEY]
                        }
                    }

                node.save()

    return JsonResponse({'message': 'success'})


def check_object_has_tr_th(request):
    """
    Check Project/Module has TestRail or TestHeader FK
    :param request:
    :return:
    """
    msg = ''
    choice = request.GET.get('choice', '')
    project_id = request.GET.get('project_id', '')
    module_id = request.GET.get('module_id', '')

    if project_id:
        project = get_object_or_404(Project, pk=project_id)
    elif module_id:
        module = get_object_or_404(Module, pk=module_id)
        project = module.project
    else:
        project = None

    if project:
        if choice == 'testheader' and not project.test_header:
            msg = 'No TestHeader'
        elif choice == 'testrail' and not project.testrail:
            msg = 'No TestRail'

    data = {
        'message': msg
    }
    return HttpResponse(json.dumps(data), content_type='application/json')
