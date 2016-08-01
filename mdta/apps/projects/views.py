import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from mdta.apps.projects.utils import context_projects

from .models import Project, Module
from .forms import ProjectNewForm, ModuleNewForm
from mdta.apps.users.models import HumanResource


@login_required
def projects(request):
    return render(request, 'projects/projects.html', context_projects())


@login_required
def project_new(request):
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
    if request.method == 'POST':
        project_id = request.POST.get('editProjectId', '')
        project_name = request.POST.get('editProjectName', '')
        project_lead = request.POST.get('editProjectLead', '')
        project_members = request.POST.getlist('editProjectMembers', '')

        project = get_object_or_404(Project, pk=project_id)
        try:
            project.name = project_name
            project.lead = get_object_or_404(HumanResource, pk=project_lead)
            project.members.clear()
            for hr_id in project_members:
                project.members.add(hr_id)

            project.save()
            messages.success(request, 'Project is updated')
        except (ValidationError, IntegrityError):
            messages.error(request, 'Edit Project Errors found')

        return redirect('projects:projects')


def fetch_project_members(request):
    data = []
    id = request.GET.get('id', '')
    project = get_object_or_404(Project, pk=id)

    for member in project.members.all():
        data.append(member.id)

    return HttpResponse(json.dumps(data), content_type='application/json')


@login_required
def module_new(request):
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