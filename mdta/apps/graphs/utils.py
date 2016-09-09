from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from mdta.apps.graphs.models import NodeType, EdgeType


NODE_TYPES_WITH_DATA = ['DataQueries Database', 'DataQueries WebService', 'Menu Prompt', 'Menu Prompt with Confirmation']
EDGE_TYPES_WITH_DATA = ['Data', 'PreCondition']


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
        subkeys = request.POST.getlist('editNodeTypeSubKeys', '')
    else:
        name = request.POST.get('editEdgeTypeName', '')
        keys = request.POST.getlist('editEdgeTypeKeys', '')
        subkeys = request.POST.getlist('editEdgeTypeSubKeys', '')

    tmp_keys = keys[0].replace(' ', '')  # remove white space from string
    tmp_subkeys = subkeys[0].replace(' ', '')

    keys_list = tmp_keys.split(',')
    subkeys_list = tmp_subkeys.split(',')

    if keys_list[-1] == '':
        del keys_list[-1]
    if len(keys_list) != len(set(keys_list)):
        messages.error(request, 'Duplicate keys found.')
        return

    if subkeys_list[-1] == '':
        del subkeys_list[-1]
    if len(subkeys_list) != len(set(subkeys_list)):
        messages.error(request, 'Dupliate subKeys found.')
        return

    try:
        node_or_edge.name = name
        node_or_edge.keys = keys_list
        node_or_edge.subkeys = subkeys_list
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


def get_properties_for_node_or_edge(request, node_or_edge_type, auto_edge=None):
    properties = {}
    tmp = {}
    if isinstance(node_or_edge_type, NodeType):
        name_list = NODE_TYPES_WITH_DATA
        key_name = 'node_'
    elif isinstance(node_or_edge_type, EdgeType):
        name_list = EDGE_TYPES_WITH_DATA
        key_name = 'edge_'
    else:
        name_list = []
        key_name = ''

    if auto_edge:
        for key in node_or_edge_type.subkeys:
            tmp[key] = request.POST.get(key_name + key, '')
        for key in node_or_edge_type.keys:
            properties[key] = request.POST.get(key_name + key, '')
    else:
        if 'DataQueries' in node_or_edge_type.name:  # Node 'DataQueries Database' and 'DataQueries WebService'
            tmp_data = get_properties_from_multi_rows(request, node_or_edge_type)
            properties[node_or_edge_type.keys_data_name] = tmp_data
            return properties

        elif 'Menu Prompt' in node_or_edge_type.name:  # Node 'Menu Prompt' and 'Menu Prompt with Confirmation'
            tmp_data = get_properties_from_multi_rows(request, node_or_edge_type)
            for key in node_or_edge_type.keys:
                properties[key] = request.POST.get(key, '')
            properties[node_or_edge_type.keys_data_name] = tmp_data
            return properties
        else:
            for key in node_or_edge_type.subkeys:
                tmp[key] = request.POST.get(key + '_0', '')
            for key in node_or_edge_type.keys:
                properties[key] = request.POST.get(key, '')

    if node_or_edge_type.name in name_list and node_or_edge_type.keys_data_name:
        properties[node_or_edge_type.keys_data_name] = tmp

    return properties


def get_properties_from_multi_rows(request, node_or_edge_type):
    data_index = request.POST.get('property_data_index', '').strip().split(' ')
    tmp_data = []
    for index in data_index:
        tmp_row = {}
        for key in node_or_edge_type.subkeys:
            tmp_row[key] = request.POST.get('{0}_{1}'.format(key, index), '')
        tmp_data.append(tmp_row)

    return tmp_data
