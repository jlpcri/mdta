from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import user_passes_test


from mdta.apps.users.views import user_is_staff
from .models import Project, ProjectDatabaseSet
from .forms import ProjectDatabaseSetNewForm
from .utils import context_project_dashboard


@user_passes_test(user_is_staff)
def project_dbset_db_new(request, project_id):
    """
    Add new Database to project dbset
    :param request:
    :param project_id:
    :return:
    """
    dbset_db = None
    if request.method == 'POST':
        form = ProjectDatabaseSetNewForm(request.POST)
        if form.is_valid():
            dbset_db = form.save()
        else:
            messages.error(request, form.errors)

    context = context_project_dashboard(request)
    context['last_tab'] = 'data_center'
    if dbset_db:
        context['last_db_id'] = dbset_db.id

    return render(request, 'projects/project_dashboard.html', context)


@user_passes_test(user_is_staff)
def project_dbset_db_edit(request):
    """
    Edit Database set name of project
    :param request:
    :param project_dbset_id:
    :return:
    """
    if request.method == 'POST':
        dbset_db_id = request.POST.get('datasetDbEditId', '')
        dbset_db_name = request.POST.get('datasetDbEditName', '')
        dbset_db = get_object_or_404(ProjectDatabaseSet, pk=dbset_db_id)
        dbset_db.name = dbset_db_name
        try:
            dbset_db.save()
        except IntegrityError:
            messages.error(request, 'Duplicate Database name')

        context = context_project_dashboard(request)
        context['last_tab'] = 'data_center'
        context['last_db_id'] = dbset_db.id

        return render(request, 'projects/project_dashboard.html', context)
