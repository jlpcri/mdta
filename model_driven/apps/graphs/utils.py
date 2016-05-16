from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import IntegrityError


def node_or_edit_type_new(request, form):
    if form.is_valid():
        form.save()
        messages.success(request, 'Node Type is added.')
    else:
        messages.error(request, form.errors)


def node_or_edge_type_edit(request, node_or_edge):
    if node_or_edge.__class__.__name__ == 'NodeType':
        name = request.POST.get('editNodeTypeName', '')
        keys = request.POST.getlist('editNodeTypeKeys', '')
    else:
        name = request.POST.get('editEdgeTypeName', '')
        keys = request.POST.getlist('editEdgeTypeKeys', '')

    keys_list = keys[0].strip().split(',')
    if keys_list[-1] == '':
        del keys_list[-1]

    try:
        node_or_edge.name = name
        node_or_edge.keys = keys_list
        node_or_edge.save()
    except (ValidationError, IntegrityError) as e:
        messages.error(request, str(e))

