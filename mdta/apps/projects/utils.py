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
