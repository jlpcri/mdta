from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from model_driven.apps.projects.models import Project
from .forms import NodeTypeNewForm, EdgeTypeNewForm


@login_required
def graphs(request):
    context = {
        'projects': Project.objects.all(),
        'node_type_new_form': NodeTypeNewForm(),
        'edge_type_new_form': EdgeTypeNewForm(),
    }
    return render(request, 'graphs/graphs.html', context)


@login_required
def node_type_new(request):
    pass


@login_required
def edge_type_new(request):
    pass
