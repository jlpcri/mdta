from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test

from mdta.apps.runner.utils import emergency_test
from mdta.apps.projects.models import TestRailInstance, Project
from mdta.apps.runner.utils import get_testrail_project, get_testrail_steps


def demo(request, project_id):
    c, f, result = emergency_test()
    return JsonResponse({'c': c, 'f': f, 'result': result})


def display_project_suites(request, project_id):
    p = Project.objects.get(id=project_id)
    trp = get_testrail_project(p.testrail.instance, p.testrail.project_id)
    suites = trp.get_suites()
    return JsonResponse({'suites': [{'name': s.name, 'id': s.id} for s in suites], 
                         'project': {'name': trp.name, 'id': trp.id}})


def display_testrail_steps(request, mdta_project_id):
    p = Project.objects.get(id=mdta_project_id)
    tri = p.testrail.instance
    case = get_testrail_steps(tri, request.GET['case_id'])
    return JsonResponse({'steps': case.custom_steps_separated})


def execute_test(request, mdta_project_id):
    p = Project.objects.get(id=mdta_project_id)
    tri = p.testrail.instance
    case = get_testrail_steps(tri, request.GET['case_id'])
    case.generate_hat_script()
    case.script.remote_user = 'caheyden'
    case.script.remote_password = 'dsi787cAH16'
    result = case.script.remote_hat_execute()
    return JsonResponse(result)


@login_required
def dashboard(request):
    p = request.user.humanresource.project
    assert p
    trp = get_testrail_project(p.testrail.instance, p.testrail.project_id)
    suites = trp.get_suites()
    for suite in suites:
        suite.cases = suite.get_cases()
    return render(request, 'runner/dashboard.html', {'project': request.user.humanresource.project,
                                                     'suites': suites})
