from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect

from testrail import APIClient, APIError

from mdta.apps.projects.models import Project, Module, TestRailInstance
from .utils import context_testcases, get_paths_through_all_edges, get_projects_from_testrail
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
        project = get_object_or_404(Project, pk=object_id)
        link_id = project.id
        testcases = create_routing_test_suite(project=project)
    elif level == 'module':
        module = get_object_or_404(Module, pk=object_id)
        link_id = module.project.id
        testcases = create_routing_test_suite(modules=[module])

    context = context_testcases()
    context['testcases'] = testcases
    context['link_id'] = link_id

    return render(request, 'testcases/testcases.html', context)


def create_routing_test_suite(project=None, modules=None):
    """
    Create routing paths for project.modules lists or module lists
    :param project:
    :param modules:
    :return:
    """
    data = []

    if project:
        data = create_routing_test_suite_module(project.modules)
    elif modules:
        data = create_routing_test_suite_module(modules)

    return data


def create_routing_test_suite_module(modules):
    """
    Create routing paths for list of modules
    :param modules:
    :return:
    """
    test_suites = []

    for module in modules:
        data = get_paths_through_all_edges(module.edges_all)

        test_suites.append({
            'module': module.name,
            'data': data
        })

    return test_suites


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
        # testrail_contents = client.send_get('get_projects')

    except AttributeError:
        print('No Testrail config')

    context = context_testcases()
    context['testrail'] = testrail_contents
    context['link_id'] = project.id

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
