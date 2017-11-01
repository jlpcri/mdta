from mdta.apps.graphs.forms import NodeTypeNewForm, EdgeTypeNewForm
from mdta.apps.graphs.models import NodeType, EdgeType
from mdta.apps.projects.forms import ProjectConfigForm, TestHeaderForm, LanguageNewForm, UploadForm, ProjectDatabaseSetNewForm
from mdta.apps.projects.models import Project, Module, TestRailConfiguration, Language
from mdta.apps.testcases.forms import TestrailConfigurationForm


def context_project_dashboard(request):
    project = request.user.humanresource.project
    projects = Project.objects.all()
    test_headers = Module.objects.filter(project=None)
    testrails = TestRailConfiguration.objects.select_related('instance').all()
    node_types = NodeType.objects.all()
    edge_types = EdgeType.objects.all()
    languages = Language.objects.all()

    project_dbset = project.projectdatabaseset_set.all()
    project_dbset_db_new_form = ProjectDatabaseSetNewForm(initial={'project': project})

    project_config_form = ProjectConfigForm(instance=project)
    testheader_new_form = TestHeaderForm()
    testrail_new_form = TestrailConfigurationForm()
    node_type_new_form = NodeTypeNewForm()
    edge_type_new_form = EdgeTypeNewForm()
    language_new_form = LanguageNewForm(initial={'project': project})
    module_import_form = UploadForm()

    context = {
        'project': project,
        'projects': projects,
        'test_headers': test_headers,
        'testrails': testrails,
        'node_types': node_types,
        'edge_types': edge_types,
        'languages': languages,

        'project_dbset': project_dbset,
        'project_dbset_db_new_form': project_dbset_db_new_form,

        'project_config_form': project_config_form,
        'testheader_new_form': testheader_new_form,
        'testrail_new_form': testrail_new_form,
        'node_type_new_form': node_type_new_form,
        'edge_type_new_form': edge_type_new_form,
        'language_new_form': language_new_form,
        'module_import_form': module_import_form,
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
