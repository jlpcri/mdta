import json

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


from mdta.apps.projects.forms import TestRunnerForm
from mdta.apps.projects.models import TestRailInstance, Project, TestRailConfiguration
from mdta.apps.runner.utils import get_testrail_project, get_testrail_steps, bulk_remote_hat_execute, bulk_hatit_file_generator, HATScript
from mdta.apps.runner.models import TestRun, AutomatedTestCase, TestServers
from mdta.apps.runner.tasks import poll_result_loop


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
    """Probably dead code. Check and refactor."""
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


def run_all_modal(request):
    if request.method == 'POST':
        testserver = request.POST.get('testserver')
        browser = request.POST.get('browser')
        apn = request.POST.get('apn')
        suite = request.POST.get('suite')
        testrail_suite_id = int(suite)
        testrail_instance = TestRailInstance.objects.first()
        project = request.user.humanresource.project
        testrail_project_id = project.testrail.project_id
        testrail_host = testrail_instance.host
        testrail_project = get_testrail_project(testrail_instance, testrail_project_id)
        testrail_suites = testrail_project.get_suites()
        testrail_suite = [s for s in testrail_suites if s.id == testrail_suite_id][0]
        testrail_cases = testrail_suite.get_cases()
        hatit_csv_filename = bulk_hatit_file_generator(testrail_cases)
        testrail_run = testrail_suite.open_test_run()
        hollytrace_url = TestServers.objects.values_list('hollytrace_url', flat=True).get(server=testserver)
        hs = HATScript()
        hs.csvfile = hatit_csv_filename
        hs.apn = apn
        hs.hatit_server = testserver
        hs.holly_server = browser
        response = hs.hatit_execute()
        mdta_test_run = TestRun.objects.create(hat_run_id=json.loads(response.text)['runid'],
                                               hat_server=TestServers.objects.get(server=testserver),
                                               testrail_project_id=testrail_project_id,
                                               testrail_suite_id=testrail_suite_id,
                                               testrail_test_run=testrail_run.id, project=project)
        poll_result_loop.delay(mdta_test_run.pk)
        for case in testrail_cases:
            print(dir(case))
            AutomatedTestCase.objects.create(test_run=mdta_test_run, testrail_case_id=case.id, case_title=case.title, case_script=case.script.body)

        return JsonResponse({'run': mdta_test_run.pk, 'holly': browser, 'tr_p_id': testrail_project_id, 'tr_host': testrail_host,
                             'hollytrace_url': hollytrace_url, 'cases': [{'testrail_case_id': c.testrail_case_id, 'status': c.status,
                                                                          'title': c.case_title, 'script': c.case_script} for c in mdta_test_run.automatedtestcase_set.all()]})
    else:
        return JsonResponse({'error': request.errors})


def check_test_result(request):
    data_list = []
    try:
        run_id = int(request.GET.get('run_id'))
        if not run_id:
            return JsonResponse({'success': False, 'reason': 'Could not read run'})
        result = AutomatedTestCase.objects.filter(test_run_id=run_id).values()
        for res in result:
            if res['status'] == 2 and res['call_id'] != '':
                data = {'status': res['status'], 'testrail_case_id': res['testrail_case_id'], 'title': res['case_title'],
                        'test_run_id': run_id, 'call_id': res['call_id'], 'tr_test_id': res['tr_test_id']}
                data_list.append(data)

            elif res['status'] == 3 and res['call_id'] != '':
                data = {'status': res['status'], 'testrail_case_id': res['testrail_case_id'], 'title': res['case_title'],
                        'test_run_id': run_id, 'call_id': res['call_id'], 'reason': res['failure_reason'],
                        'tr_test_id': res['tr_test_id']}
                data_list.append(data)

        return JsonResponse({'success': True, 'running': False, 'data': data_list})
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
