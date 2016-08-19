import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from mdta.apps.projects.utils import context_projects

from .models import Project, Module
from .forms import ProjectForm, ModuleForm


@login_required
def projects(request):
    """
    View of apps/projects
    :param request:
    :return:
    """
    return render(request, 'projects/projects.html', context_projects())


@login_required
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
            messages.success(request, 'Project is added.')

            return redirect('projects:projects')
        else:
            messages.error(request, form.errors)

            context = {
                'form': form
            }

            return render(request, 'projects/project_new.html', context)


@login_required
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
        try:
            project = form.save()
            return redirect('projects:projects')
        except Exception as e:
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


@login_required
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


@login_required
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
            except Exception as e:
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


