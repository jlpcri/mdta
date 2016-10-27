from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test

from mdta.apps.runner.utils import emergency_test
from mdta.apps.projects.models import TestRailInstance, Project
from mdta.apps.runner.utils import get_testrail_project

def demo(request, project_id):
    c, f, result = emergency_test()
    return JsonResponse({'c': c, 'f': f, 'result': result})

def display_project_suites(request, project_id):
    p = Project.objects.get(id=project_id)
    trp = get_testrail_project(p.testrail.instance, p.testrail.project_id)
    suites = trp.get_suites()
    return JsonResponse({'suites': [{'name': s.name, 'id': s.id} for s in suites], 
                         'project': {'name': trp.name, 'id': trp.id}})

@login_required
def dashboard(request):
    assert(request.user.humanresource.project)
    return render(request, 'runner/dashboard.html', {'project': request.user.humanresource.project})
