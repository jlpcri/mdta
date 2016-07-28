from django.shortcuts import redirect, get_object_or_404

from mdta.apps.projects.models import Project, Module


def create_testcases(request, object_id):
    level = request.GET.get('level', '')
    if level == 'project':
        project = get_object_or_404(Project, pk=object_id)
        create_routing_test_suite(project)
    elif level == 'module':
        module = get_object_or_404(Module, pk=object_id)
        create_routing_test_suite(modules=[module])

    return redirect('projects:projects')


def create_routing_test_suite(project=None, modules=None):
    if project:
        print(project.start_nodes)
    elif modules:
        for module in modules:
            print(module.start_nodes)