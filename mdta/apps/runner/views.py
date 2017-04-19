import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test

from mdta.apps.projects.forms import TestRunnerForm
from mdta.apps.projects.models import TestRailInstance, Project, TestRailConfiguration
from mdta.apps.runner.utils import get_testrail_project, get_testrail_steps, bulk_remote_hat_execute, check_result, bulk_hatit_file_generator, HATScript


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
    case.script.remote_user = 'wicqacip'
    case.script.remote_password = 'LogFiles'
    result = case.script.remote_hat_execute()
    return JsonResponse(result)


def run_test_suite(request):
    testrail_suite_id = int(request.GET['suite'])
    testrail_instance = TestRailInstance.objects.first()
    project = request.user.humanresource.project
    testrail_project_id = project.testrail.project_id
    testrail_project = get_testrail_project(testrail_instance, testrail_project_id)
    testrail_suites = testrail_project.get_suites()
    testrail_suite = [s for s in testrail_suites if s.id == testrail_suite_id][0]
    testrail_cases = testrail_suite.get_cases()
    files_to_monitor = bulk_remote_hat_execute(testrail_cases)
    return JsonResponse({'success': True, 'scripts': files_to_monitor})


def run_test_suite_in_hatit(request):
    testrail_suite_id = int(request.GET['suite'])
    print(testrail_suite_id)
    testrail_instance = TestRailInstance.objects.first()
    project = request.user.humanresource.project
    testrail_project_id = project.testrail.project_id
    testrail_project = get_testrail_project(testrail_instance, testrail_project_id)
    testrail_suites = testrail_project.get_suites()
    testrail_suite = [s for s in testrail_suites if s.id == testrail_suite_id][0]
    testrail_cases = testrail_suite.get_cases()
    hatit_csv_filename = bulk_hatit_file_generator(testrail_cases)
    # with open(hatit_csv_filename) as csv_file:
    #     response = HttpResponse(csv_file.read(), content_type='text/csv')
    #     response['Content-Disposition'] = 'attachment; filename="{0}"'.format(hatit_csv_filename)
    # return response
    print(hatit_csv_filename)
    return {'success': True, 'scripts': hatit_csv_filename}


def run_all_modal(request):
    if request.method == 'POST':
        form = TestRunnerForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print(data)
            # hs = HATScript()
            # hs.apn = data.get('apn')
            # print(hs.apn)
            # hs.holly_server = data.get('browser')
            # print(hs.holly_server)
            # hs.basic_connection_test()
            # response = hs.hatit_execute()
            # print(hs.results())
        else:
            print(form.errors)

    return {'success': True}


def check_test_result(request):
    try:
        filename = request.GET.get('filename', False)
        if not filename:
            return JsonResponse({'success': False, 'reason': 'Could not read filename'})
        response = check_result(filename)
        if response:
            response['running'] = False
            return JsonResponse(response)
        return JsonResponse({'running': True})
    except Exception as e:
        return JsonResponse({'success': False, 'reason': 'An untrapped error occurred: ' + str(e.args)})


@login_required
def dashboard(request):
    p = request.user.humanresource.project
    assert p
    try:
        trp = get_testrail_project(p.testrail.instance, p.testrail.project_id)
    except AttributeError:
        p.testrail = TestRailConfiguration.objects.first()
        trp = get_testrail_project(p.testrail.instance, p.testrail.project_id)
    suites = trp.get_suites()
    for suite in suites:
        suite.cases = suite.get_cases()
    return render(request, 'runner/dashboard.html', {'project': request.user.humanresource.project,
                                                     'suites': suites,
                                                     'modal_run_all': TestRunnerForm()})


