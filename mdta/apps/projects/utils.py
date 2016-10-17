from mdta.apps.graphs.models import NodeType, EdgeType
from mdta.apps.projects.forms import ProjectConfigForm
from mdta.apps.projects.forms import TestHeaderForm
from mdta.apps.projects.models import Project, Module, TestRailConfiguration
from mdta.apps.testcases.forms import TestrailConfigurationForm


def context_project_dashboard(request):
    project = request.user.humanresource.project
    test_headers = Module.objects.filter(project=None)
    testrails = TestRailConfiguration.objects.all()
    node_types = NodeType.objects.all()
    edge_types = EdgeType.objects.all()

    project_config_form = ProjectConfigForm(instance=project)
    testheader_new_form = TestHeaderForm()
    testrail_new_form = TestrailConfigurationForm()

    context = {
        'project': project,
        'test_headers': test_headers,
        'testrails': testrails,
        'node_types': node_types,
        'edge_types': edge_types,

        'project_config_form': project_config_form,
        'testheader_new_form': testheader_new_form,
        'testrail_new_form': testrail_new_form,
    }

    return context


def context_projects():
    """
    Retrieve context for tab projects
    :return:
    """
    context = {
        'projects': Project.objects.all(),
        'test_headers': Module.objects.filter(project=None)
    }

    return context


def check_testheader_duplicate(test_header_name, test_headers):
    for item in test_headers:
        if item.name == test_header_name:
            return True

    return False
