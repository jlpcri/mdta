from mdta.apps.graphs.models import Node, Edge

START_NODE_NAME = ['Start', 'TestHeader Start']
DATA_NODE_NAME = ['DataQueries Database', 'DataQueries WebService']
CONSTRAINTS_TRUE_OR_FALSE = 'tof'
TESTCASE_NOT_ROUTE_MESSAGE = 'This edge cannot be routed'


def path_traverse_backwards(path, th_path=None):
    """
    Traverse path backwards to generate test steps
    :param path: route path
    :param th_path: test header path
    :return:
    """
    tcs = []
    tcs_cannot_route = ''
    constraints = []
    pre_conditions = []
    match_constraint_found = False

    path.reverse()

    for index, step in enumerate(path):
        if index < len(path) - 1:
            if isinstance(step, Node):
                if step.type.name in DATA_NODE_NAME and not match_constraint_found:
                    result_found = get_data_node_result(step, constraints, index=index, path=path)
                    if result_found:
                        match_constraint_found = True
                        # update next step content as found result from Data Node
                        update_tcs_next_step_content(tcs, result_found)
                    else:
                        tcs_cannot_route = TESTCASE_NOT_ROUTE_MESSAGE
                        break
                else:
                    traverse_node(step, tcs, preceding_edge=path[index + 1])
            elif isinstance(step, Edge):
                if step.type.name == 'Data':
                    constraints += assert_current_edge_constraint(step)
                    constraints += assert_high_priority_edges_negative(step)

                pre_condition = assert_precondition(step)
                if pre_condition not in pre_conditions:
                    pre_conditions += pre_condition
        else:
            if th_path:
                # th_path.reverse()
                for th_index, th_step in enumerate(th_path[::-1]):
                    if th_index < len(th_path) - 1:
                        if isinstance(th_step, Node):
                            traverse_node(th_step, tcs, th_path[th_index + 1])
                    else:
                        if isinstance(th_step, Node):
                            traverse_node(th_step, tcs)
            traverse_node(step, tcs)

    if tcs_cannot_route:
        data = {
            'tcs_cannot_route': tcs_cannot_route
        }
    else:
        tcs.reverse()
        data = {
            'pre_conditions': pre_conditions,
            'tc_steps': tcs,
        }
    return data


def get_data_node_result(node, constraints, index=None, path=None):
    """
    Get result from DataQueries Node
    :param node: DataQueries Node
    :param constraints: Constraints of current test case
    :param index: index of current Node
    :param path: route path
    :return:
    """
    dicts = node.properties[node.type.keys_data_name]
    data = {}
    compare_key = ''

    if len(constraints) > 0:
        found_current_node = False
        for each in dicts:
            found = True
            for constraint in constraints:
                for key in constraint.keys():
                    if key != CONSTRAINTS_TRUE_OR_FALSE:
                        compare_key = key
                try:
                    if constraint[CONSTRAINTS_TRUE_OR_FALSE] == 'True' \
                            and each['Outputs'][compare_key] != constraint[compare_key]:
                        found = False
                        break
                    elif constraint[CONSTRAINTS_TRUE_OR_FALSE] == 'False' \
                            and each['Outputs'][compare_key] == constraint[compare_key]:
                        found = False
                        break
                except Exception as e:
                    found = False

            if found:
                found_current_node = True
                try:
                    data = each['Inputs']
                except Exception as e:
                    print(e)
                    pass
                break
        if not found_current_node:
            for pre_index, pre_step in enumerate(path[(index + 1):]):
                if isinstance(pre_step, Node) and pre_step.type.name in DATA_NODE_NAME:
                    data = get_data_node_result(pre_step, constraints, index=pre_index, path=path[(index + 1):])
                    break

    return data


def assert_current_edge_constraint(edge):
    """
    Assert current edge constraints
    :param edge:
    :return:
    """
    data = []
    current_edge_constraints = get_edge_constraints(edge, rule='True')
    data += current_edge_constraints

    return data


def assert_high_priority_edges_negative(edge):
    """
    Assert edge with high priority from leaving edges of from node
    :param edge:
    :return:
    """
    data = []
    edges = edge.from_node.leaving_edges.exclude(id=edge.id)
    for each_edge in edges:
        if each_edge.priority < edge.priority:
            data += get_edge_constraints(each_edge, rule='False')

    return data


def assert_precondition(edge):
    """
    Assert PreCondition of edge of test case
    :param edge:
    :return:
    """
    data = []
    edges = edge.from_node.leaving_edges
    for each_edge in edges:
        if each_edge.type.name == 'PreCondition':
            tmp = ''
            dicts = each_edge.properties[each_edge.type.keys_data_name][each_edge.type.subkeys_data_name]
            if each_edge.id == edge.id:
                operator = ' = '
            else:
                operator = ' != '
            for key in dicts:
                tmp = key + operator + dicts[key]

            data.append(tmp)

    return data


def get_edge_constraints(item, rule):
    """
    Get constraints from edge
    :param item:
    :param rule:
    :return:
    """
    data = []
    for key in item.properties:
        if key == 'OutputData':
            try:
                # print(item.properties[key][item.type.subkeys_data_name])
                for constraint_key in item.properties[key][item.type.subkeys_data_name].keys():
                    tmp = {
                        constraint_key: item.properties[key][item.type.subkeys_data_name][constraint_key],
                        CONSTRAINTS_TRUE_OR_FALSE: rule  # True or False
                    }
                    data.append(tmp)
            except (KeyError, TypeError) as e:
                print(e)
                pass
    # print(data)
    return data


def update_tcs_next_step_content(tcs, result_found):
    """
    Update test case next step contents
    :param tcs:
    :param result_found:
    :return:
    """
    if len(tcs) > 0:
        step = tcs[-1]
        for k in result_found:
            step['content'] = 'press ' + result_found[k]


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
    if node.type.name in [START_NODE_NAME[0], 'Transfer']:  # Start with Dial Number
        add_step(node_start(node), tcs)
    elif node.type.name in ['Menu Prompt', 'Menu Prompt with Confirmation', 'Play Prompt']:
        add_step(node_prompt(node, preceding_edge), tcs)


def node_start(node):
    return {
        'content': get_item_properties(node),
    }


def node_prompt(node, preceding_edge=None, match_constraint=None):
    content = ''
    if match_constraint:
        content = 'press ' + match_constraint
    elif preceding_edge:
        if preceding_edge.type.name == 'DTMF':
            try:
                content = 'press ' + preceding_edge.properties['Press']
            except KeyError:
                content = 'press '
        elif preceding_edge.type.name == 'Speech':
            try:
                content = 'say ' + preceding_edge.properties['Say']
            except KeyError:
                content = 'say '

    return {
        'content': content,
        'expected': "{0}: {1}".format(node.name, node.properties['Verbiage'])
    }


def get_item_properties(item):
    data = ''
    for key in item.properties:
        # if key == 'InputData':
        #     try:
        #         for ele in item.properties[key]:
        #             data += 'Inputs: ' + str(ele['Inputs']) + ', Outputs: ' + str(ele['Outputs']) + '; '
        #     except (KeyError, TypeError):
        #         data += key
        # elif key == 'OutputData':
        #     try:
        #         data += str(item.properties[key][item.type.subkeys_data_name])
        #     except KeyError:
        #         data += key
        # else:
        try:
            data += key + ': ' + item.properties[key] + ', '
        except (KeyError, TypeError):
            data += key

    return data
