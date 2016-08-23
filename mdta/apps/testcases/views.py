from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect

from testrail import APIClient, APIError

from mdta.apps.projects.models import Project, Module, TestRailInstance, TestRailConfiguration
from mdta.apps.testcases.models import TestCaseResults
from mdta.apps.testcases.tasks import create_testcases_celery
from .utils import context_testcases, get_projects_from_testrail, create_routing_test_suite
from .forms import TestrailConfigurationForm


@login_required
def testcases(request):
    context = context_testcases()

    return render(request, 'testcases/testcases.html', context)


@login_required
def create_testcases(request, object_id):
    """
    Create TestCases per project/module
    :param request:
    :param object_id: project_id/module_id
    :return:
    """

    testcases = []
    link_id = ''
    level = request.GET.get('level', '')
    if level == 'project':
        create_testcases_celery(object_id)

    elif level == 'module':
        module = get_object_or_404(Module, pk=object_id)
        link_id = module.project.id
        testcases = create_routing_test_suite(modules=[module])

    context = context_testcases()
    context['testcases'] = testcases
    context['link_id'] = link_id

    return render(request, 'testcases/testcases.html', context)


@login_required
def demonstrate_testcases(request, object_id):
    """
    Demonstrate TestCases of Project/Module from TestCaseResults
    :param request:
    :param object_id:
    :return:
    """
    level = request.GET.get('level', '')
    if level == 'project':
        project = get_object_or_404(Project, pk=object_id)
        link_id = project.id
        try:
            testcases = project.testcaseresults_set.latest('updated').results
        except TestCaseResults.DoesNotExist:
            testcases = []
    elif level == 'module':
        module = get_object_or_404(Module, pk=object_id)
        link_id = module.project.id
        try:
            tmp_tcs = module.project.testcaseresults_set.latest('updated').results
            testcases = [(item for item in tmp_tcs if item['module'] == module.name).__next__()]
        except TestCaseResults.DoesNotExist:
            testcases = []
    else:
        testcases = []
        link_id = ''

    context = context_testcases()
    context['testcases'] = testcases
    context['link_id'] = link_id

    return render(request, 'testcases/testcases.html', context)


@login_required
def push_testcases_to_testrail(request, project_id):
    """
    Push Testcases of project to TestRail
    :param request:
    :param project_id:
    :return:
    """
    project = get_object_or_404(Project, pk=project_id)
    testrail_contents = ''

    try:
        client = APIClient(project.testrail.instance.host)
        client.user = project.testrail.instance.username
        client.password = project.testrail.instance.password

        testrail_contents = client.send_get('get_project/' + project.testrail.project_id)
        # testrail_contents_case = client.send_get('get_case/23896')

    except AttributeError:
        print('No Testrail config')

    context = context_testcases()
    context['testrail'] = testrail_contents
    context['link_id'] = project.id

    # for item in testrail_contents_case['custom_steps_seperated']:
    #     print(item)

    return render(request, 'testcases/testcases.html', context)


@login_required
def testrail_configuration_new(request):
    if request.method == 'GET':
        context = {
            'form': TestrailConfigurationForm()
        }
        return render(request, 'testcases/tc_testrails_new.html', context)
    elif request.method == 'POST':
        # print(request.POST)

        instance = get_object_or_404(TestRailInstance, username='testrail@west.com')
        testrail_projects = get_projects_from_testrail(instance)

        form = TestrailConfigurationForm(request.POST)
        if form.is_valid():
            testrail_new = form.save(commit=False)
            testrail_find = next(item for item in testrail_projects if item['name'] == testrail_new.project_name)
            testrail_new.project_id = testrail_find['id']
            testrail_new.test_suite = []

            testrail_new.save()
        else:
            messages.error(request, form.errors)

        return redirect('testcases:testcases')


@login_required
def testrail_configuration_delete(request, testrail_id):
    testrail = get_object_or_404(TestRailConfiguration, pk=testrail_id)

    testrail.delete()

    return redirect('testcases:testcases')
