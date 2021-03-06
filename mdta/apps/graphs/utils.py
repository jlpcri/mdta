import ast
import json
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from mdta.apps.graphs.models import NodeType, EdgeType
from mdta.apps.testcases.constant_names import NODE_DATA_NAME as NODE_TYPES_WITH_DATA, NODE_SET_VARIABLE,\
    EDGE_DATA_NAME, EDGE_PRECONDITION_NAME, EDGE_TYPES_INVISIBLE_KEY, NODE_POSITIONS_KEY, NODE_X_KEY, NODE_Y_KEY, \
    NODE_X_INITIAL, NODE_Y_INITIAL


# NODE_TYPES_WITH_DATA = ['DataQueries Database', 'DataQueries WebService']
EDGE_TYPES_WITH_DATA = [EDGE_DATA_NAME, EDGE_PRECONDITION_NAME]
# EDGE_TYPES_INVISIBLE_KEY = 'Invisible'


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
        verbiage_keys = request.POST.getlist('editNodeTypeVerbiageKeys', '')
    else:
        name = request.POST.get('editEdgeTypeName', '')
        keys = request.POST.getlist('editEdgeTypeKeys', '')
        subkeys = request.POST.getlist('editEdgeTypeSubKeys', '')
        verbiage_keys = ''

    tmp_keys = keys[0].replace(' ', '')  # remove white space from string
    tmp_subkeys = subkeys[0].replace(' ', '')

    keys_list = tmp_keys.split(',')
    subkeys_list = tmp_subkeys.split(',')

    if verbiage_keys:
        tmp_verbiage_keys = verbiage_keys[0].replace(' ', '')
        verbiage_keys_list = tmp_verbiage_keys.split(',')
    else:
        verbiage_keys_list = []

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
        if verbiage_keys_list:
            node_or_edge.verbiage_keys = verbiage_keys_list
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
                        'type': edge.type.name,
                        'to_node': edge.to_node.name,
                        'from_node': edge.from_node.name,
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
                        'type': edge.type.name,
                        'to_node': edge.to_node.name,
                        'from_node': edge.from_node.name,
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
        if 'DataQueries' in node_or_edge_type.name:  # Node 'DataQueries Database' and 'DataQueries WebService'
            tmp_data = get_properties_from_multi_rows(request, node_or_edge_type, key_name)
            properties[node_or_edge_type.keys_data_name] = tmp_data
        elif node_or_edge_type.name in EDGE_TYPES_WITH_DATA and isinstance(node_or_edge_type, EdgeType) or node_or_edge_type.name == NODE_SET_VARIABLE:
            properties = get_properties_from_other_json(request, key_name + node_or_edge_type.subkeys_data_name, node_or_edge_type)
        else:
            for key in node_or_edge_type.subkeys:
                tmp[key] = request.POST.get(key_name + key + '_0', '')
            for key in node_or_edge_type.keys:
                properties[key] = request.POST.get(key_name + key, '')
            if node_or_edge_type.name in name_list and node_or_edge_type.keys_data_name:
                properties[node_or_edge_type.keys_data_name] = tmp
    else:
        if 'DataQueries' in node_or_edge_type.name:  # Node 'DataQueries Database' and 'DataQueries WebService'
            tmp_data = get_properties_from_multi_rows(request, node_or_edge_type)
            properties[node_or_edge_type.keys_data_name] = tmp_data
        elif node_or_edge_type.name in EDGE_TYPES_WITH_DATA and isinstance(node_or_edge_type, EdgeType) or node_or_edge_type.name == NODE_SET_VARIABLE:
            properties = get_properties_from_other_json(request, node_or_edge_type.subkeys_data_name, node_or_edge_type)
        else:
            for key in node_or_edge_type.subkeys:
                tmp[key] = request.POST.get(key + '_0', '')
            for key in node_or_edge_type.keys:
                properties[key] = request.POST.get(key, '')

            if node_or_edge_type.name in name_list and node_or_edge_type.keys_data_name:
                properties[node_or_edge_type.keys_data_name] = tmp

    return properties


def get_properties_from_multi_rows(request, node_or_edge_type, key_name=None):
    if key_name:
        data_index = request.POST.get(key_name + 'property_data_index', '').strip().split(' ')
    else:
        data_index = request.POST.get('property_data_index', '').strip().split(' ')

    tmp_data = []
    for index in data_index:
        tmp_row = {}
        for key in node_or_edge_type.subkeys:
            key_data = {}
            try:
                if key_name:
                    key_data_json = ast.literal_eval(request.POST.get(key_name + '{0}_{1}'.format(key, index), ''))
                else:
                    key_data_json = ast.literal_eval(request.POST.get('{0}_{1}'.format(key, index), ''))
                for d_key in key_data_json:
                    key_data[d_key] = key_data_json[d_key]
            except Exception as e:
                pass

            tmp_row[key] = key_data

        tmp_data.append(tmp_row)

    return tmp_data


def get_properties_from_other_json(request, request_input, item_type):
    properties = {}
    key_data = {}
    subkey_data = {}

    try:
        key_data_json = ast.literal_eval(request.POST.get(request_input + '_0', ''))
        for d_key in key_data_json:
            subkey_data[d_key] = key_data_json[d_key]
        key_data[item_type.subkeys_data_name] = subkey_data
        for key in item_type.keys:
            if key == EDGE_TYPES_INVISIBLE_KEY:
                properties[key] = request.POST.get(key, '')
            else:
                properties[key] = key_data
    except Exception:
        for key in item_type.keys:
            if key == EDGE_TYPES_INVISIBLE_KEY:
                properties[key] = request.POST.get(key, '')
            else:
                properties[key] = {
                    item_type.subkeys_data_name: ''
                }

    return properties


def node_related_edges_invisible(node, module):
    """
    Check edges of node which is outside current module to current module are all invisible
    :param node: Node outside of current module
    :param module: Current module
    :return: True or False
    """
    flag, flag_arriving, flag_leaving = True, False, False

    for edge in node.arriving_edges:
        try:
            if edge.properties[EDGE_TYPES_INVISIBLE_KEY] != 'on' and edge.from_node.module == module:
                flag_arriving = True
                break
        except KeyError:
            pass

    for edge in node.leaving_edges:
        try:
            if edge.properties[EDGE_TYPES_INVISIBLE_KEY] != 'on' and edge.to_node.module == module:
                flag_leaving = True
                break
        except KeyError:
            pass

    if flag_arriving or flag_leaving:
        flag = False

    return flag


def self_reference_edge_node_in_set(edge, network_edges, edge_reference_sizes):
    found = False
    size_found = False
    size = 20

    for item in network_edges:
        if item['from'] == item['to']:
            if item['from'] == edge.from_node.id:
                found = True
                for each_size in edge_reference_sizes:
                    if each_size['node_id'] == item['from']:
                        each_size['size'] += 10
                        size = each_size['size']
                        size_found = True
                        break
                else:
                    edge_reference_sizes.append({
                        'node_id': item['from'],
                        'size': 20
                    })

                if size_found:
                    break
    else:
        edge_reference_sizes.append({
            'node_id': edge.from_node.id,
            'size': 20
        })

    data = {
        'flag': found,
        'size': size
    }

    return data


def get_positions_for_node(request, node):
    positions_new = request.POST.get(NODE_POSITIONS_KEY, '')
    if positions_new:
        positions_new = json.loads(positions_new)
        if NODE_POSITIONS_KEY in node.properties:
            positions_old = node.properties[NODE_POSITIONS_KEY]
            for item in positions_old:
                if item == positions_new['module_id']:
                    positions_old[item][NODE_X_KEY] = positions_new['positions']['x']
                    positions_old[item][NODE_Y_KEY] = positions_new['positions']['y']
        else:
            positions_old = {
                positions_new['module_id']: {
                    NODE_X_KEY: positions_new['positions']['x'],
                    NODE_Y_KEY: positions_new['positions']['y']
                }
            }
    else:
        positions_old = {
            node.module.id: {
                NODE_X_KEY: NODE_X_INITIAL,
                NODE_Y_KEY: NODE_Y_INITIAL
            }
        }

    return positions_old