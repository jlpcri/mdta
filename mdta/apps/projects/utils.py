from mdta.apps.projects.forms import ProjectNewForm, ModuleNewForm
from mdta.apps.projects.models import Project
from mdta.apps.users.models import HumanResource


def context_projects():
    context = {
        'projects': Project.objects.all(),
        'project_new_form': ProjectNewForm(),
        'module_new_form': ModuleNewForm(),
        'hrs': HumanResource.objects.all(),
    }

    return context