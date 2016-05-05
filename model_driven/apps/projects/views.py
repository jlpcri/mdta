from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404

from .models import Project
from .forms import ProjectNewForm
from model_driven.apps.users.models import HumanResource


@login_required
def projects(request):
    context = {
        'projects': Project.objects.all(),
        'project_new_form': ProjectNewForm(),
        'hrs': HumanResource.objects.all(),
    }
    return render(request, 'projects/projects.html', context)


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
        project_worker = request.POST.getlist('editProjectWorker', '')

        project = get_object_or_404(Project, pk=project_id)
        try:
            project.name = project_name
            project.lead = get_object_or_404(HumanResource, pk=project_lead)
            project.worker.clear()
            for hr_id in project_worker:
                project.worker.add(hr_id)

            project.save()
            messages.success(request, 'Project is updated')
        except (ValidationError, IntegrityError):
            messages.error(request, 'Edit Project Errors found')

        return redirect('projects:projects')