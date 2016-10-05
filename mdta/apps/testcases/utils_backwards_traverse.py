from mdta.apps.graphs.models import Node, Edge

START_NODE_NAME = ['Start', 'TestHeader Start']


def path_traverse_backwards(path):
    tcs = []
    constraints = []
    path.reverse()

    for index, step in enumerate(path):
        if index < len(path) - 1:
            if isinstance(step, Node):
                traverse_node(step, tcs, path[index + 1])
            elif isinstance(step, Edge):
                # traverse_edge(step, tcs)
                if step.type.name == 'Data':
                    constraints += assert_data_edge_constraint(step)
        else:
            traverse_node(step, tcs)

    tcs.reverse()
    for tc in tcs:
        print(tc)

    print(constraints)


def add_step(step, tcs):
    """
    Add step to test cases
    :param step:
    :param tcs:
    :return:
    """
    tcs.append({
        'content': step['content'],
        'expected': step['expected'] if 'expected' in step.keys() else ''
    })


def traverse_node(node, tcs, preceding_edge=None):
    """
    Traverse Node based on node type
    :param node:
    :param tcs:
    :return:
    """
    if node.type.name == START_NODE_NAME[0]:  # Start with Dial Number
        add_step(node_start(node), tcs)
    elif node.type.name in ['Menu Prompt', 'Menu Prompt with Confirmation', 'Play Prompt']:
        add_step(node_prompt(node, preceding_edge), tcs)
    elif node.type.name in ['TestHeader Start', 'TestHeader End']:
        pass
    else:
        add_step(node_check_holly_log(node), tcs)


def node_start(node):
    return {
        'content': get_item_properties(node),
    }


def node_prompt(node, preceding_edge=None):
    content = ''
    if preceding_edge:
        if preceding_edge.type.name == 'DTMF':
            content = 'press ' + preceding_edge.properties['Number']
        elif preceding_edge.type.name == 'Speech':
            content = preceding_edge.properties['Response']

    return {
        'content': content,
        'expected': node.properties['Verbiage']
    }


def node_check_holly_log(node):
    if node.properties:
        data = {
            'content': 'Node - ' + node.name + ', ' + get_item_properties(node)
        }
    else:
        data = {
            'content': 'Node - ' + node.name
        }

    return data


def assert_data_edge_constraint(edge):
    data = [get_item_properties(edge)] + assert_high_priority_edges_avoid(edge)

    return data


def assert_high_priority_edges_avoid(edge):
    data = []
    edges = edge.from_node.leaving_edges.exclude(id=edge.id)
    for each_edge in edges:
        if each_edge.priority < edge.priority:
            data.append(get_item_constraints(each_edge))

    return data


def get_item_constraints(item):
    data = ''
    for key in item.properties:
        if key == 'OutputData':
            print(type(item.properties[key][item.type.subkeys_data_name]))
            print(item.properties[key][item.type.subkeys_data_name])
            try:
                for subkey in item.properties[key][item.type.subkeys_data_name]:
                    data += subkey + ': ' + item.properties[key][item.type.subkeys_data_name][subkey]
            except (KeyError, TypeError):
                pass


def get_item_properties(item):
    data = ''
    for key in item.properties:
        if key == 'InputData':
            try:
                for ele in item.properties[key]:
                    data += 'Inputs: ' + str(ele['Inputs']) + ', Outputs: ' + str(ele['Outputs']) + '; '
            except (KeyError, TypeError):
                data += key
        elif key == 'OutputData':
            try:
                data += str(item.properties[key][item.type.subkeys_data_name])
            except KeyError:
                data += key
        else:
            try:
                data += key + ': ' + item.properties[key] + ', '
            except (KeyError, TypeError):
                data += key

    return data