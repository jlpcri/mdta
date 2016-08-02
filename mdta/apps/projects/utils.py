from mdta.apps.projects.forms import ProjectNewForm, ModuleNewForm
from mdta.apps.projects.models import Project, TestRailConfiguration, CatalogItem
from mdta.apps.users.models import HumanResource


def context_projects():
    context = {
        'projects': Project.objects.all(),
        'project_new_form': ProjectNewForm(),
        'module_new_form': ModuleNewForm(),
        'hrs': HumanResource.objects.all(),

        'testrails': TestRailConfiguration.objects.all(),
        'catalogs': CatalogItem.objects.all()
    }

    return context
