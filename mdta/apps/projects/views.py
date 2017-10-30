import json
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
import socket

from mdta.apps.projects.utils import context_project_dashboard, context_projects, check_testheader_duplicate
from mdta.apps.users.views import user_is_staff, user_is_superuser
from .models import Project, Module, Language
from .forms import ProjectForm, ModuleForm, TestHeaderForm, ProjectConfigForm, LanguageNewForm


@user_passes_test(user_is_staff)
def project_dashboard(request):
    """
    View of project dashboard, include project config, testheader config,
    testrail config, node type config, edge type config
    :param request:
    :return:
    """
    context = context_project_dashboard(request)

    if context['project']:
        return render(request, 'projects/project_dashboard.html', context)
    else:
        return redirect('graphs:projects_for_selection')


@user_passes_test(user_is_staff)
def project_config(request, project_id):
    if request.method == 'POST':
        project = get_object_or_404(Project, pk=project_id)
        form = ProjectConfigForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
        else:
            messages.error(request, form.errors)

        return redirect('projects:project_dashboard')


@user_passes_test(user_is_staff)
def projects(request):
    """
    View of apps/projects
    :param request:
    :return:
    """
    return render(request, 'projects/projects.html', context_projects())


@user_passes_test(user_is_staff)
def project_new(request):
    """
    Add new project
    :param request:
    :return:
    """
    if request.method == 'GET':
        form = ProjectForm()

        context = {
            'form': form
        }

        return render(request, 'projects/project_new.html', context)

    elif request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            hr = request.user.humanresource
            hr.project = project
            hr.save()

            messages.success(request, 'Project is added.')

            return redirect('home')
        else:
            messages.error(request, form.errors)

            context = {
                'form': form
            }

            return render(request, 'projects/project_new.html', context)


@user_passes_test(user_is_staff)
def project_edit(request, project_id):
    """
    Edit project
    :param request:
    :return:
    """
    project = get_object_or_404(Project, pk=project_id)

    if request.method == 'GET':
        form = ProjectForm(instance=project)
        context = {
            'project': project,
            'form': form
        }

        return render(request, 'projects/project_edit.html', context)
    elif request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        # print(request.POST)
        try:
            if 'project_edit' in request.POST:
                project = form.save()
            elif socket.gethostname() == 'sliu-OptiPlex-GX520' and 'project_delete' in request.POST:
                project.humanresource_set.clear()
                project.save()
                project.delete()
            return redirect('projects:projects')
        except ValueError as e:
            messages.error(request, str(e))

            context = {
                'project': project,
                'form': form
            }

            return render(request, 'projects/project_edit.html', context)


def fetch_project_catalogs_members(request):
    """
    Get catalogs and members of project for new/edit project
    :param request:
    :return:
    """
    data = {}
    catalogs = []
    catalogs_module = []
    members = []
    object_id = request.GET.get('id', '')
    level = request.GET.get('level', '')

    if level == 'project':
        project = get_object_or_404(Project, pk=object_id)

        for catalog in project.catalog.all():
            catalogs.append(catalog.id)
            catalogs_module.append({
                'id': catalog.id,
                'name': catalog.name
            })

        for member in project.members.all():
            members.append(member.id)

        data = {
            'catalogs': catalogs,
            'catalogs_module': catalogs_module,
            'members': members
        }
    elif level == 'module':
        module = get_object_or_404(Module, pk=object_id)

        for catalog in module.catalog.all():
            catalogs.append(catalog.id)

        data = {
            'catalogs': catalogs
        }

    return HttpResponse(json.dumps(data), content_type='application/json')


@user_passes_test(user_is_staff)
def module_new(request):
    """
    Add new module of project
    :param request:
    :return:
    """
    if request.method == 'GET':
        form = ModuleForm()
        context = {
            'form': form
        }

        return render(request, 'projects/module_new.html', context)
    elif request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            module = form.save()
            messages.success(request, 'Module \'{0}\' is added to \'{1}\''.format(module.name, module.project.name))

            return redirect('projects:projects')
        else:
            messages.error(request, form.errors)

            context = {
                'form': form
            }

            return render(request, 'projects/module_new.html', context)


@user_passes_test(user_is_staff)
def module_edit(request, module_id):
    """
    Edit module of project
    :param request:
    :return:
    """
    module = get_object_or_404(Module, pk=module_id)
    if request.method == 'GET':
        form = ModuleForm(instance=module)
        context = {
            'module': module,
            'form': form
        }

        return render(request, 'projects/module_edit.html', context)
    elif request.method == 'POST':
        if 'module_save' in request.POST:
            form = ModuleForm(request.POST, instance=module)
            try:
                module = form.save()
                messages.success(request, 'Module is saved.')
                return redirect('projects:projects')
            except ValueError as e:
                messages.error(request, str(e))

                context = {
                    'module': module,
                    'form': form
                }

                return render(request, 'projects/module_edit.html', context)
        elif 'module_delete' in request.POST:
            module = get_object_or_404(Module, pk=module_id)
            module.delete()

            return redirect('projects:projects')


@user_passes_test(user_is_staff)
def test_header_new(request):
    """
    Add new Test Header as Module which project is null
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = TestHeaderForm(request.POST)
        if form.is_valid():
            test_header = form.save(commit=False)
            test_headers = Module.objects.filter(project=None).exclude(pk=test_header.id)
            if check_testheader_duplicate(test_header.name, test_headers):
                messages.error(request, 'Test Header name duplicated')
            else:
                test_header = form.save()
                messages.success(request, 'Test Header {0} is added'.format(test_header.name))
        else:
            messages.error(request, form.errors)

        context = context_project_dashboard(request)
        context['last_tab'] = 'test_headers'

        return render(request, 'projects/project_dashboard.html', context)


@user_passes_test(user_is_staff)
def test_header_edit(request):
    """
    Edit Test Header
    :param request:
    :return:
    """
    if request.method == 'POST':
        test_header_id = request.POST.get('editTestHeaderId', '')
        test_header_name = request.POST.get('editTestHeaderName', '')
        test_header = get_object_or_404(Module, pk=test_header_id)

        if 'test_header_save' in request.POST:
            test_headers = Module.objects.filter(project=None).exclude(pk=test_header.id)
            try:
                if check_testheader_duplicate(test_header_name, test_headers):
                    messages.error(request, 'Test Header name duplicated')
                else:
                    test_header.name = test_header_name
                    test_header.save()
                    messages.success(request, 'Test Header is saved.')
            except ValueError as e:
                messages.error(request, str(e))

        elif 'test_header_delete' in request.POST:
            test_header.delete()

        context = context_project_dashboard(request)
        context['last_tab'] = 'test_headers'

        return render(request, 'projects/project_dashboard.html', context)


@user_passes_test(user_is_staff)
def language_new(request):
    if request.method == 'POST':
        form = LanguageNewForm(request.POST)
        if form.is_valid():
            language = form.save()
        else:
            messages.error(request, form.errors)

    context = context_project_dashboard(request)
    context['last_tab'] = 'languages'

    return render(request, 'projects/project_dashboard.html', context)


@user_passes_test(user_is_staff)
def language_edit(request):
    if request.method == 'POST':
        language_id = request.POST.get('editLanguageId', '')
        project_id = request.POST.get('editLanguageProject', '')
        name = request.POST.get('editLanguageName', '')
        root_path = request.POST.get('editLanguageRootPath', '')

        language = get_object_or_404(Language, pk=language_id)
        language.project_id = project_id
        language.name = name
        language.root_path = root_path
        language.save()

    context = context_project_dashboard(request)
    context['last_tab'] = 'languages'

    return render(request, 'projects/project_dashboard.html', context)


@user_passes_test(user_is_superuser)
def project_data_migrate(request, project_id):
    """
    Migrate Project, All Projects, All TestHeaders data
    :param request:
    :param project_id:
    :return:
    """
    if request.user.username not in ['sliu', 'mambati']:
        return redirect('intro')

    type_migrate = request.GET.get('type', '')
    if type_migrate == 'all':
        projs = Project.objects.all()
        for p in projs:
            # print(p.name)
            project_data_migrate_single(p)
    elif type_migrate == 'th':
        ths = Module.objects.filter(project=None)
        for th in ths:
            if th.name:
                project_data_migrate_nodes(th.nodes)
                project_data_migrate_edges(th.edges_all)
            else:
                th.delete()
    else:
        project = get_object_or_404(Project, pk=project_id)
        # print(project.name)
        project_data_migrate_single(project)

    return redirect('projects:projects')


def project_data_migrate_single(project):
    """
    Migrate Project Nodes and Edges
    :param project:
    :return:
    """
    project_data_migrate_nodes(project.nodes)
    project_data_migrate_edges(project.edges)


def project_data_migrate_nodes(nodes):
    """
    Migrate Nodes data
    :param nodes:
    :return:
    """
    for node in nodes:
        if 'Prompt' in node.type.name:
            tmp_property, tmp_verbiage = {}, {}
            for key in node.type.keys:
                try:
                    tmp_property[key] = node.properties[key]
                except (KeyError, TypeError):
                    tmp_property[key] = ''
            for key in node.type.verbiage_keys:
                try:
                    if key == 'InitialPrompt':
                        tmp_verbiage[key] = node.properties['Verbiage']
                    else:
                        tmp_property[key] = node.properties[key]
                except (KeyError, TypeError):
                    tmp_verbiage[key] = ''

            # print(node.properties)
            # print(tmp_property)

            node.properties = tmp_property
            if not node.verbiage:
                node.verbiage = {'English': tmp_verbiage}
            try:
                node.save()
            except ValidationError:
                print(node.name, node)

        if node.type.name == 'Start':
            tmp_property = {}
            for key in node.type.keys:
                if key == 'APN':
                    try:
                        tmp_property[key] = node.properties[key]
                    except (KeyError, TypeError):
                        try:
                            tmp_property[key] = node.properties['DialedNumber']
                        except (KeyError, TypeError):
                            tmp_property[key] = ''
                else:
                    try:
                        tmp_property[key] = node.properties[key]
                    except (KeyError, TypeError):
                        tmp_property[key] = ''

            # print(node.properties, tmp_property)
            node.properties = tmp_property
            node.save()

        if 'DataQueries' in node.type.name:
            tmp_property = {}
            for key in node.type.keys:
                try:
                    tmp_property[key] = node.properties[key]
                except KeyError:
                    tmp_property[key] = ''

            node.properties = tmp_property
            node.save()


def project_data_migrate_edges(edges):
    """
    Migrate Edges data
    :param edges:
    :return:
    """
    for edge in edges:
        if edge.type.name in ['DTMF', 'Speech']:
            tmp_property = {}
            for key in edge.type.keys:
                try:
                    tmp_property[key] = edge.properties[key]
                except (KeyError, TypeError):
                    tmp_property[key] = ''

            # print(edge.properties)
            # print(tmp_property)
            # print('----------------')
            edge.properties = tmp_property
            edge.save()


@user_passes_test(user_is_staff)
def language_new_from_module_import(request):
    data = []
    if request.method == 'POST':
        lan = json.loads(request.POST.get('lan', ''))
        project_id = lan['project_id']
        project = get_object_or_404(Project, pk=project_id)

        lan_obj = Language.objects.create(
            name=lan['name'],
            root_path=lan['root_path'],
            project=project
        )
        data = project.language_lists

    return HttpResponse(json.dumps(data), content_type='application/json')


@user_passes_test(user_is_staff)
def get_language_detail_for_import_module(request):
    data = []
    if request.method == 'GET':
        lan_id = request.GET.get('lan_id', '')
        lan = get_object_or_404(Language, pk=lan_id)
        data = {
            'lan_name': lan.name,
            'root_path': lan.root_path
        }

    return HttpResponse(json.dumps(data), content_type='application/json')
