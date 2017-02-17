from mdta.apps.graphs.models import Node, Edge
from mdta.apps.testcases.constant_names import *


def path_traverse_backwards(path, th_path=None):
    """
    Traverse path backwards to generate test steps
    :param path: route path
    :param th_path: test header path
    :return:
    """
    tcs = []
    tcs_cannot_route_msg = ''
    constraints = []
    pre_conditions = []
    # match_constraint_found = False
    tcs_cannot_route_flag = False

    if th_path:
        th_menu_prompt_outputs_keys = get_menu_prompt_outputs_key(path=None, index_start=None, th_path=th_path)
    else:
        th_menu_prompt_outputs_keys = []

    path.reverse()

    result_found_all = []

    # sibling_edges_key_in_th_menuprompt = []

    for index, step in enumerate(path):
        if index < len(path) - 1:
            if isinstance(step, Node):
                if step.type.name not in NODE_DATA_NAME:
                    traverse_node(step, tcs, preceding_edge=path[index + 1])
            elif isinstance(step, Edge):
                if step.type.name == EDGE_DATA_NAME:
                    if step.from_node.leaving_edges.count() > 1:
                        if non_data_edge_has_higher_priority(step):
                            tcs_cannot_route_flag = True
                            tcs_cannot_route_msg = 'Non Data Edge has higher priority.'
                            break

                    if edge_property_key_in_th_menuprompt(step, th_path):
                        result_found = step.properties[step.type.keys_data_name][step.type.subkeys_data_name]
                        menu_prompt_outputs_keys = list(step.properties[step.type.keys_data_name][step.type.subkeys_data_name].keys())

                    elif edge_property_key_in_from_menuprompt(step):
                        result_found = step.properties[step.type.keys_data_name][step.type.subkeys_data_name]
                        menu_prompt_outputs_keys = [step.from_node.properties[MP_OUTPUTS]]
                    else:
                        constraints += assert_current_edge_constraint(step)
                        constraints += assert_high_priority_edges_negative(step)

                        result_found = get_data_node_result(step, constraints, index=index, path=path)
                        menu_prompt_outputs_keys = get_menu_prompt_outputs_key(path, index, th_path=None)
                    if result_found:
                        result_found_all.append(result_found)
                        constraints = []

                        # menu_prompt_outputs_keys = get_menu_prompt_outputs_key(path, index, th_path=None)
                        # print('r: ', result_found, step.to_node.name)
                        # print('s: ', menu_prompt_outputs_keys)

                        if menu_prompt_outputs_keys:
                            # update next step content as found result from Data Node
                            test_success = update_tcs_next_step_content(tcs=tcs,
                                                                        result_found=result_found,
                                                                        menu_prompt_outputs_keys=menu_prompt_outputs_keys)
                            if not test_success['Success']:
                                tcs_cannot_route_flag = True
                                tcs_cannot_route_msg = 'MenuPrompt/MenuPromptWC property \'Outputs\' incorrect'
                        else:
                            tcs_cannot_route_flag = True
                            tcs_cannot_route_msg = 'MenuPrompt/MenuPromptWC property \'Outputs\' not found'
                    else:
                        tcs_cannot_route_flag = True
                        tcs_cannot_route_msg = 'No match result found in DataQueries Node'
                        if not th_menu_prompt_outputs_keys:
                            break

                elif step.from_node.leaving_edges.count() > 1:
                    for edge in step.from_node.leaving_edges.exclude(id=step.id):
                        if edge.type.name == EDGE_DATA_NAME:
                            current_edges_key_in_th_menuprompt = edge_property_key_in_th_menuprompt(edge, th_path)
                            if current_edges_key_in_th_menuprompt and edge.priority < step.priority:
                                # sibling_edges_key_in_th_menuprompt.append(current_edges_key_in_th_menuprompt)
                                # print(edge.properties[edge.type.keys_data_name][edge.type.subkeys_data_name])
                                break

                pre_condition = assert_precondition(step)
                if pre_condition and pre_condition not in pre_conditions:
                    pre_conditions += pre_condition
        else:
            if len(result_found_all) > 0:
                result_found = result_found_all[0]
            else:
                result_found = None
            # print('t: ', result_found)
            if th_path:
                # th_path.reverse()
                for th_index, th_step in enumerate(th_path[::-1]):
                    if th_index < len(th_path) - 1:
                        if isinstance(th_step, Node):
                            if th_step.type.name in NODE_MP_NAME:
                                th_key = th_step.properties[MP_OUTPUTS]
                                if result_found and th_key:
                                    if th_key in result_found.keys():
                                        result = result_found
                                        # Then this test case can be routed
                                        tcs_cannot_route_flag = False
                                    else:
                                        result = {th_key: th_step.properties[MP_DEFAULT]}
                                    update_tcs_next_step_content(tcs=tcs,
                                                                 result_found=result,
                                                                 test_header=True)
                                else:
                                    if th_step.properties[MP_DEFAULT]:
                                        result = {th_key: th_step.properties[MP_DEFAULT]}
                                        update_tcs_next_step_content(tcs=tcs,
                                                                     result_found=result,
                                                                     test_header=True)
                                    else:
                                        tcs_cannot_route_flag = True
                                        tcs_cannot_route_msg = 'TestHeader Node \'{0}: Default\' empty'.format(th_step.name)

                            traverse_node(th_step, tcs, th_path[::-1][th_index + 1])
                    else:
                        if isinstance(th_step, Node):
                            traverse_node(th_step, tcs)

                # traverse Start Node
                if th_path[2].type.name in NODE_MP_NAME:
                    tcs[-1][TR_CONTENT] = get_item_properties(step)
                else:
                    traverse_node(step, tcs)

    if tcs_cannot_route_flag:
        data = {
            'tcs_cannot_route': TESTCASE_NOT_ROUTE_MESSAGE + ': ' + tcs_cannot_route_msg
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
                            and each[MP_OUTPUTS][compare_key] != constraint[compare_key]:
                        found = False
                        break
                    elif constraint[CONSTRAINTS_TRUE_OR_FALSE] == 'False' \
                            and each[MP_OUTPUTS][compare_key] == constraint[compare_key]:
                        found = False
                        break
                except Exception as e:
                    found = False

            if found:
                found_current_node = True
                try:
                    data = each[NODE_DATA_INPUTS]
                except Exception as e:
                    print(e)
                    pass
                break
        if not found_current_node:
            for pre_index, pre_step in enumerate(path[(index + 1):]):
                if isinstance(pre_step, Node) and pre_step.type.name in NODE_DATA_NAME:
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
        if each_edge.type.name == EDGE_PRECONDITION_NAME:
            tmp = ''
            dicts = each_edge.properties[each_edge.type.keys_data_name][each_edge.type.subkeys_data_name]
            if each_edge.id == edge.id:
                operator = ' = '
            else:
                operator = ' != '
            for key in dicts:
                tmp = key + operator + str(dicts[key])

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
        if key == EDGE_OUTPUTDATA_NAME:
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


def get_menu_prompt_outputs_key(path, index_start, th_path):
    """
    Search Menu Prompt / Menu Prompt with Confirmation, fetch node.properties['Outputs']
    as key in Data Node inputs key
    :param path:
    :param index_start:
    :return:
    """
    keys = []
    if th_path:
        for step in th_path[::-1]:
            if step.type.name in NODE_MP_NAME:
                keys.append(step.properties[MP_OUTPUTS])
    else:
        for index, step in enumerate(path[index_start:]):
            if step.type.name in NODE_MP_NAME:
                keys.append(step.properties[MP_OUTPUTS])
                break

    return keys


def update_tcs_next_step_content(tcs, result_found, menu_prompt_outputs_keys=None, test_header=None):
    """
    Update test case next step contents
    :param tcs:
    :param result_found:
    :param menu_prompt_outputs_keys: node.properties['Outputs']
    :return:
    """
    # print(test_header, result_found)
    key_found = True
    if menu_prompt_outputs_keys:
        keys = [x.strip() for x in menu_prompt_outputs_keys[0].split(',')]

        for key in keys:
            if key not in result_found.keys():
                key_found = False
                break
    else:
        key_found = False

    if key_found or test_header:
        if len(tcs) > 0:
            step = tcs[-1]
            if len(result_found) == 1:
                for k in result_found:
                    step[TR_CONTENT] = 'press ' + str(result_found[k])
            else:
                tmp = 'press '
                for k in result_found:
                    tmp += k + ':' + str(result_found[k]) + ', '
                step[TR_CONTENT] = tmp
        data = {'Success': True}
    else:
        data = {'Success': False}

    return data


def add_step(step, tcs):
    """
    Add step to test cases
    :param step:
    :param tcs:
    :return:
    """
    tcs.append({
        'content': step[TR_CONTENT],
        'expected': step[TR_EXPECTED] if 'expected' in step.keys() else ''
    })


def traverse_node(node, tcs, preceding_edge=None):
    """
    Traverse Node based on node type
    :param node:
    :param tcs:
    :return:
    """
    if node.type.name in [NODE_START_NAME[0], 'Transfer']:  # Start with Dial Number
        add_step(node_start(node), tcs)
    elif node.type.name in NODE_MP_NAME + [NODE_PLAY_PROMPT_NAME]:
        add_step(node_prompt(node, preceding_edge), tcs)

    if node.type.name == NODE_MP_NAME[1]:
        confirm_idx = 0
        for idx, tc in enumerate(tcs):
            if node.name in tc[TR_EXPECTED]:
                confirm_idx = idx
                break
        if confirm_idx > 0:
            content = tcs[confirm_idx - 1][TR_CONTENT]
            tcs[confirm_idx - 1][TR_CONTENT] = 'press 1'  # confirm input
            tcs.insert(confirm_idx, {
                'content': content,
                'expected': "{0}: {1}".format(node.name, node.properties[MP_CVER])
            })


def node_start(node):
    return {
        'content': get_item_properties(node),
    }


def node_prompt(node, preceding_edge=None, match_constraint=None):
    content = ''
    if match_constraint:
        content = 'press ' + match_constraint
    elif preceding_edge:
        if preceding_edge.type.name == EDGE_DTMF_NAME:
            try:
                content = 'press ' + preceding_edge.properties[EDGE_PRESS_NAME]
            except KeyError:
                content = 'press '
        elif preceding_edge.type.name == EDGE_SPEECH_NAME:
            try:
                content = 'say ' + preceding_edge.properties[EDGE_SAY_NAME]
            except KeyError:
                content = 'say '

    return {
        'content': content,
        'expected': "{0}: {1}".format(node.name, node.properties[MP_VER])
    }


def get_item_properties(item):
    data = ''
    for key in item.properties:
        try:
            data += key + ': ' + item.properties[key] + ', '
        except (KeyError, TypeError):
            data += key

    return data


def edge_property_key_in_th_menuprompt(step, th_path):
    """
    check current step property key is in test header menuprompt Outputs
    :param step:
    :param th_path:
    :return:
    """
    data = ''
    step_key = list(step.properties[step.type.keys_data_name][step.type.subkeys_data_name].keys())[0]
    for th_step in th_path:
        if th_step.type.name in NODE_MP_NAME and step_key == th_step.properties[MP_OUTPUTS]:
            data = step_key
            break

    return data


def edge_property_key_in_from_menuprompt(step):
    """
    check current step property key is in from node(menuprompt) Outputs
    :param step:
    :return:
    """
    data = False

    step_key = list(step.properties[step.type.keys_data_name][step.type.subkeys_data_name].keys())[0]
    if step.from_node.type.name in NODE_MP_NAME and step.from_node.properties[MP_OUTPUTS] == step_key:
        data = True

    return data


def non_data_edge_has_higher_priority(step):
    """
    Check if edge has sibling edges which is Non data Edge and has higher priority
    :param step: edge
    :return:
    """
    find = False
    for edge in step.from_node.leaving_edges.exclude(id=step.id):
        if edge.type.name != EDGE_DATA_NAME and edge.priority < step.priority:
            find = True
            break

    return find
