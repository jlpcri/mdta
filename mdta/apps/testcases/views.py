from django.shortcuts import get_object_or_404, render

from mdta.apps.projects.models import Project, Module
from mdta.apps.projects.utils import context_projects
from .utils import get_paths_through_all_edges


def create_testcases(request, object_id):
    """
    Create TestCases per project/module
    :param request:
    :param object_id: project_id/module_id
    :return:
    """

    testcases = []
    level = request.GET.get('level', '')
    if level == 'project':
        project = get_object_or_404(Project, pk=object_id)
        testcases = create_routing_test_suite(project=project)
    elif level == 'module':
        module = get_object_or_404(Module, pk=object_id)
        testcases = create_routing_test_suite(modules=[module])

    context = context_projects()
    context['testcases'] = testcases
    # print(testcases)

    return render(request, 'projects/projects.html', context)


def create_routing_test_suite(project=None, modules=None):
    """
    Create routing paths for project.modules lists or module lists
    :param project:
    :param modules:
    :return:
    """
    data = []

    if project:
        # data = create_routing_test_suite_project(project)
        data = create_routing_test_suite_module(project.modules)
    elif modules:
        data = create_routing_test_suite_module(modules)

    return data


def create_routing_test_suite_project(project):
    """
    Create routing paths for project
    :param project:
    :return:
    """
    test_suites = []
    data = get_paths_through_all_edges(project.edges)

    test_suites.append({
        'project': project.name,
        'data': data
    })

    return test_suites


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



