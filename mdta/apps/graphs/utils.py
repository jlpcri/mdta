from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import IntegrityError


def node_or_edge_type_new(request, form):
    """
    Add new Node/Edge Type form action
    :param request:
    :param form:
    :return:
    """
    if form.is_valid():
        keys = form.cleaned_data['keys']
        if len(keys) != len(set(keys)):
            messages.error(request, 'Duplicate keys found.')
            return

        form.save()
        messages.success(request, 'Node Type is added.')
    else:
        messages.error(request, form.errors)


def node_or_edge_type_edit(request, node_or_edge):
    """
    Edit Node/Edge Type form action
    :param request:
    :param node_or_edge:
    :return:
    """
    if node_or_edge.__class__.__name__ == 'NodeType':
        name = request.POST.get('editNodeTypeName', '')
        keys = request.POST.getlist('editNodeTypeKeys', '')
    else:
        name = request.POST.get('editEdgeTypeName', '')
        keys = request.POST.getlist('editEdgeTypeKeys', '')

    tmp = keys[0].replace(' ', '')  # remove white space from string

    keys_list = tmp.split(',')
    if keys_list[-1] == '':
        del keys_list[-1]

    if len(keys_list) != len(set(keys_list)):
        messages.error(request, 'Duplicate keys found.')
        return

    try:
        node_or_edge.name = name
        node_or_edge.keys = keys_list
        node_or_edge.save()
    except (ValidationError, IntegrityError) as e:
        messages.error(request, str(e))


def check_edge_in_set(edge, network_edges):
    """
    Check if edge in network_edges(edges from between modules)
    :param edge:
    :param network_edges:
    :return:
    """
    found = False
    for item in network_edges:
        # Found the edges between two same modules
        if item['from'] == edge.from_node.module.id and item['to'] == edge.to_node.module.id:
            item['label'] += 1
            if 'edge_list' in item:
                item['edge_list'].append(
                    {
                        'id': edge.id,
                        'edge_name': edge.from_node.name + '-' + edge.to_node.name,
                        'type': edge.type.id,
                        'to_node': edge.to_node.id,
                        'from_node': edge.from_node.id,
                        'priority': edge.priority,
                        'properties': edge.properties
                    }
                )
            else:
                item['edge_list'] = [
                    {
                        'id': item['id'],
                        'edge_name': item['edge_name'],
                        'type': item['type'],
                        'to_node': item['to_node'],
                        'from_node': item['from_node'],
                        'priority': item['priority'],
                        'properties': item['properties']
                    },
                    {
                        'id': edge.id,
                        'edge_name': edge.from_node.name + '-' + edge.to_node.name,
                        'type': edge.type.id,
                        'to_node': edge.to_node.id,
                        'from_node': edge.from_node.id,
                        'priority': edge.priority,
                        'properties': edge.properties
                    }
                ]

            found = True
            break

    return found




