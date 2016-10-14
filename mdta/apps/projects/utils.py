from mdta.apps.projects.models import Project, Module


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
