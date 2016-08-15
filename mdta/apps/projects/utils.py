from mdta.apps.projects.models import Project


def context_projects():
    """
    Retrieve context for tab projects
    :return:
    """
    context = {
        'projects': Project.objects.all(),
    }

    return context
