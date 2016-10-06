from mdta.apps.graphs.models import Node, Edge

START_NODE_NAME = ['Start', 'TestHeader Start']
CONSTRAINTS_TRUE_OR_FALSE = 'tof'


def path_traverse_backwards(path):
    data = {}
    tcs = []
    constraints = []
    path.reverse()

    for index, step in enumerate(path):
        if index < len(path) - 1:
            if isinstance(step, Node):
                if step.type.name in ['DataQueries Database', 'DataQueries WebService']:
                    result_found = get_data_node_result(step, constraints)
                    constraints.append(result_found)
                else:
                    traverse_node(step, tcs, path[index + 1])
            elif isinstance(step, Edge):
                # traverse_edge(step, tcs)
                if step.type.name == 'Data':
                    constraints += assert_current_edge_constraint(step)
                    constraints += assert_high_priority_edges_negative(step)
        else:
            traverse_node(step, tcs)

    tcs.reverse()

    data = {
        'constraints': constraints,
        'tc_steps': tcs,
    }
    return data


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
    # elif node.type.name in ['TestHeader Start', 'TestHeader End']:
    #     pass
    # else:
    #     add_step(node_check_holly_log(node), tcs)


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


def get_data_node_result(node, constraints):
    dicts = node.properties[node.type.keys_data_name]
    data = {}
    compare_key = ''

    for each in dicts:
        found = True
        for constraint in constraints:
            for key in constraint.keys():
                if key != CONSTRAINTS_TRUE_OR_FALSE:
                    compare_key = key
            if constraint[CONSTRAINTS_TRUE_OR_FALSE] == 'True' \
                    and each['Outputs'][compare_key] != constraint[compare_key]:
                found = False
                break
            elif constraint[CONSTRAINTS_TRUE_OR_FALSE] == 'False' \
                    and each['Outputs'][compare_key] == constraint[compare_key]:
                found = False
                break

        if found:
            data = each['Inputs']
            break

    return data


def assert_current_edge_constraint(edge):
    data = [get_edge_constraints(edge, rule='True')]

    return data


def assert_high_priority_edges_negative(edge):
    data = []
    edges = edge.from_node.leaving_edges.exclude(id=edge.id)
    for each_edge in edges:
        if each_edge.priority < edge.priority:
            data.append(get_edge_constraints(each_edge, rule='False'))

    return data


def get_edge_constraints(item, rule):
    data = {}
    for key in item.properties:
        if key == 'OutputData':
            try:
                for constraint_key in item.properties[key][item.type.subkeys_data_name]:
                    data = {
                        constraint_key: item.properties[key][item.type.subkeys_data_name][constraint_key],
                        CONSTRAINTS_TRUE_OR_FALSE: rule  # True or False
                    }

            except (KeyError, TypeError) as e:
                print(e.messages)
                pass
    return data


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