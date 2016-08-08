import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from mdta.apps.projects.utils import context_projects

from .models import Project, Module, TestRailConfiguration
from .forms import ProjectNewForm, ModuleNewForm
from mdta.apps.users.models import HumanResource


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
    if request.method == 'POST':
        form = ProjectNewForm(request.POST)
        if form.is_valid():
            project = form.save()
            messages.success(request, 'Project is added.')
        else:
            messages.error(request, 'Errors found')

        return redirect('projects:projects')


@login_required
def project_edit(request):
    """
    Edit project
    :param request:
    :return:
    """
    if request.method == 'POST':
        project_id = request.POST.get('editProjectId', '')
        project_name = request.POST.get('editProjectName', '')
        project_testrail = request.POST.get('editProjectTestrail', '')
        project_catalog = request.POST.getlist('editProjectCatalogs', '')
        project_lead = request.POST.get('editProjectLead', '')
        project_members = request.POST.getlist('editProjectMembers', '')

        project = get_object_or_404(Project, pk=project_id)
        try:
            project.name = project_name
            if project_lead:
                project.lead = get_object_or_404(HumanResource, pk=project_lead)

            if project_testrail:
                project.testrail = get_object_or_404(TestRailConfiguration, pk=project_testrail)

            project.catalog.clear()
            for catalog_id in project_catalog:
                project.catalog.add(catalog_id)

            project.members.clear()
            for hr_id in project_members:
                project.members.add(hr_id)

            project.save()
            messages.success(request, 'Project is updated')
        except (ValidationError, IntegrityError):
            messages.error(request, 'Edit Project Errors found')

        return redirect('projects:projects')


def fetch_project_catalogs_members(request):
    """
    Get catalogs and members of project for new/edit project
    :param request:
    :return:
    """
    catalogs = []
    catalogs_module = []
    members = []
    id = request.GET.get('id', '')
    project = get_object_or_404(Project, pk=id)

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

    return HttpResponse(json.dumps(data), content_type='application/json')


@login_required
def module_new(request):
    """
    Add new module of project
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = ModuleNewForm(request.POST)
        if form.is_valid():
            module = form.save()
            messages.success(request, 'Module \'{0}\' is added to \'{1}\''.format(module.name, module.project.name))
        else:
            messages.error(request, 'Errors found.')

        return redirect('projects:projects')


@login_required
def module_edit(request):
    """
    Edit module of project
    :param request:
    :return:
    """
    if request.method == 'POST':
        module_id = request.POST.get('editModuleId', '')
        module_name = request.POST.get('editModuleName', '')
        module_project = request.POST.get('editModuleProject', '')

        module = get_object_or_404(Module, pk=module_id)
        try:
            module.name = module_name
            module.project.id = module_project
            module.save()
            messages.success(request, 'Module is saved.')
        except Exception as e:
            messages.error(request, str(e))

        return redirect('projects:projects')