import random

from mdta.apps.testcases.constant_names import *


def tc_no_input_recover(node):
    """
    Test step of No Input and recover to self
    :return:
    """
    data = [
        {
            TR_CONTENT: 'wait',
            TR_EXPECTED: node.name + 'NI1: ' + node.properties[MP_NI1]
        }
    ]

    return data


def tc_confirm_no_input_recover(node):
    """
    Test step of Confirm No Input and recover to self for MenuPromptWithConfirmation node
    :param node:
    :return:
    """
    data = [
        {
            TR_CONTENT: get_mpc_valid_input(node),
            TR_EXPECTED: node.name + ': ' + node.properties[MP_CVER]
        },
        {
            TR_CONTENT: 'wait',
            TR_EXPECTED: node.name + 'CNI1: ' + node.properties[MP_CNI1]
        }
    ]

    return data


def tc_no_match_recover(node):
    """
    Test step of No Match and recover to self
    :return:
    """
    no_match_content = get_no_match_content(node)
    data = [
        {
            TR_CONTENT: no_match_content,
            TR_EXPECTED: node.name + 'NM1: ' + node.properties[MP_NM1]
        }
    ]

    return data


def tc_confirm_no_match_recover(node):
    """
    Test step of Confirm No Match and recover to self for MenuPromptWithConfirmation node
    :param node:
    :return:
    """
    data = [
        {
            TR_CONTENT: get_mpc_valid_input(node),
            TR_EXPECTED: node.name + ': ' + node.properties[MP_CVER]
        },
        {
            TR_CONTENT: get_no_match_content(node),
            TR_EXPECTED: node.name + 'CNM1: ' + MP_CNM1
        }
    ]

    return data


def tc_no_input_3_fail(node):
    """
    Test step of 3 times No Input then Fail
    :return:
    """
    data = []
    if node.properties[ON_FAIL_GO_TO_KEY] == '':
        data.append({
            TR_CONTENT: False,
            TR_EXPECTED: TESTCASE_NOT_ROUTE_MESSAGE + ', OnFailGoTo empty'
        })
    elif not search_node_name_inside_project(node.module.project, node.properties[ON_FAIL_GO_TO_KEY]):
        data.append({
            TR_CONTENT: False,
            TR_EXPECTED: TESTCASE_NOT_ROUTE_MESSAGE + ', OnFailGoTo node name invalid'
        })
    else:
        data.append({
            TR_CONTENT: 'wait',
            TR_EXPECTED: node.name + 'NI1: ' + node.properties[MP_NI1]
        })
        data.append({
            TR_CONTENT: 'wait',
            TR_EXPECTED: node.name + 'NI2: ' + node.properties[MP_NI2]
        })
        data.append({
            TR_CONTENT: 'wait',
            TR_EXPECTED: 'Test fail, route to: ' + node.properties[ON_FAIL_GO_TO_KEY]
        })

    return data


def tc_confirm_no_input_3_fail(node):
    if node.properties[ON_FAIL_GO_TO_KEY] == '':
        data = [{
            TR_CONTENT: False,
            TR_EXPECTED: TESTCASE_NOT_ROUTE_MESSAGE + ', OnFailGoTo empty'
        }]
    elif not search_node_name_inside_project(node.module.project, node.properties[ON_FAIL_GO_TO_KEY]):
        data = [{
            TR_CONTENT: False,
            TR_EXPECTED: TESTCASE_NOT_ROUTE_MESSAGE + ', OnFailGoTo node name invalid'
        }]
    else:
        data = [
            {
                TR_CONTENT: get_mpc_valid_input(node),
                TR_EXPECTED: node.name + ': ' + node.properties[MP_CVER]
            },
            {
                TR_CONTENT: 'wait',
                TR_EXPECTED: node.name + 'CNI1: ' + node.properties[MP_CNI1]
            },
            {
                TR_CONTENT: 'wait',
                TR_EXPECTED: node.name + 'CNI2: ' + node.properties[MP_CNI2]
            },
            {
                TR_CONTENT: 'wait',
                TR_EXPECTED: 'Test fail, route to: ' + node.properties[ON_FAIL_GO_TO_KEY]
            },
        ]

    return data


def tc_no_match_3_fail(node):
    """
    Test step of 3 times No Match then Fail
    :return:
    """
    data = []

    if node.properties[ON_FAIL_GO_TO_KEY] == '':
        data.append({
            TR_CONTENT: False,
            TR_EXPECTED: TESTCASE_NOT_ROUTE_MESSAGE + ', OnFailGoTo empty'
        })
    elif not search_node_name_inside_project(node.module.project, node.properties[ON_FAIL_GO_TO_KEY]):
        data.append({
            TR_CONTENT: False,
            TR_EXPECTED: TESTCASE_NOT_ROUTE_MESSAGE + ', OnFailGoTo node name invalid'
        })
    else:
        no_match_content = get_no_match_content(node)
        data.append({
            TR_CONTENT: no_match_content,
            TR_EXPECTED: node.name + 'NM1: ' + node.properties[MP_NM1]
        })

        no_match_content = get_no_match_content(node)
        data.append({
            TR_CONTENT: no_match_content,
            TR_EXPECTED: node.name + 'NM2: ' + node.properties[MP_NM2]
        })

        no_match_content = get_no_match_content(node)
        data.append({
            TR_CONTENT: no_match_content,
            TR_EXPECTED: 'Test fail, route to: ' + node.properties[ON_FAIL_GO_TO_KEY]
        })

    return data


def tc_confirm_no_match_3_fail(node):
    if node.properties[ON_FAIL_GO_TO_KEY] == '':
        data = [{
            TR_CONTENT: False,
            TR_EXPECTED: TESTCASE_NOT_ROUTE_MESSAGE + ', OnFailGoTo empty'
        }]
    elif not search_node_name_inside_project(node.module.project, node.properties[ON_FAIL_GO_TO_KEY]):
        data = [{
            TR_CONTENT: False,
            TR_EXPECTED: TESTCASE_NOT_ROUTE_MESSAGE + ', OnFailGoTo node name invalid'
        }]
    else:
        data = [
            {
                TR_CONTENT: get_mpc_valid_input(node),
                TR_EXPECTED: node.name + ': ' + node.properties[MP_CVER]
            },
            {
                TR_CONTENT: get_no_match_content(node),
                TR_EXPECTED: node.name + 'CNM1: ' + node.properties[MP_CNM1]
            },
            {
                TR_CONTENT: get_no_match_content(node),
                TR_EXPECTED: node.name + 'CNM2: ' + node.properties[MP_CNM2]
            },
            {
                TR_CONTENT: get_no_match_content(node),
                TR_EXPECTED: 'Test fail, route to: ' + node.properties[ON_FAIL_GO_TO_KEY]
            },
        ]

    return data


def tc_ni_nm_3_fail(node):
    """
    Test step of 3 times 'No Input' or 'No Match' then Fail
    :return:
    """
    data = []
    ni_index = 0
    nm_index = 0

    if node.properties[ON_FAIL_GO_TO_KEY] == '':
        data.append({
            TR_CONTENT: False,
            TR_EXPECTED: TESTCASE_NOT_ROUTE_MESSAGE + ', OnFailGoTo empty'
        })
    elif not search_node_name_inside_project(node.module.project, node.properties[ON_FAIL_GO_TO_KEY]):
        data.append({
            TR_CONTENT: False,
            TR_EXPECTED: TESTCASE_NOT_ROUTE_MESSAGE + ', OnFailGoTo node name invalid'
        })
    else:
        combinations = random_combination(random_size=3)
        for index, item in enumerate(combinations):
            if item == 'NI':
                content = 'wait'
                ni_index += 1
                if index >= 2:
                    expected = 'Test fail, route to: ' + node.properties[ON_FAIL_GO_TO_KEY]
                else:
                    expected = node.name + 'NI{0}: '.format(ni_index) + node.properties['NoInput_{0}'.format(ni_index)]
            else:
                content = get_no_match_content(node)
                nm_index += 1
                if index >= 2:
                    expected = 'Test fail, route to: ' + node.properties[ON_FAIL_GO_TO_KEY]
                else:
                    expected = node.name + 'NM{0}: '.format(nm_index) + node.properties['NoMatch_{0}'.format(nm_index)]
            data.append({
                TR_CONTENT: content,
                TR_EXPECTED: expected
            })

    return data


def tc_confirm_ni_nm_3_fail(node):
    data = []
    ni_index = 0
    nm_index = 0

    if node.properties[ON_FAIL_GO_TO_KEY] == '':
        data.append({
            TR_CONTENT: False,
            TR_EXPECTED: TESTCASE_NOT_ROUTE_MESSAGE + ', OnFailGoTo empty'
        })
    elif not search_node_name_inside_project(node.module.project, node.properties[ON_FAIL_GO_TO_KEY]):
        data.append({
            TR_CONTENT: False,
            TR_EXPECTED: TESTCASE_NOT_ROUTE_MESSAGE + ', OnFailGoTo node name invalid'
        })
    else:
        data.append({
            TR_CONTENT: get_mpc_valid_input(node),
            TR_EXPECTED: node.name + ': ' + node.properties[MP_CVER]
        })
        combinations = random_combination(random_size=3)
        for index, item in enumerate(combinations):
            if item == 'NI':
                content = 'wait'
                ni_index += 1
                if index >= 2:
                    expected = 'Test fail, route to: ' + node.properties[ON_FAIL_GO_TO_KEY]
                else:
                    expected = node.name + 'CNI{0}: '.format(ni_index) + node.properties['ConfirmNoInput_{0}'.format(ni_index)]
            else:
                content = get_no_match_content(node)
                nm_index += 1
                if index >= 2:
                    expected = 'Test fail, route to: ' + node.properties[ON_FAIL_GO_TO_KEY]
                else:
                    expected = node.name + 'CNM{0}: '.format(nm_index) + node.properties['ConfirmNoMatch_{0}'.format(nm_index)]
            data.append({
                TR_CONTENT: content,
                TR_EXPECTED: expected
            })

    return data


def get_negative_tc_steps(key):
    """
    Simulate switch case, call related function followed by key
    :param key:
    :return:
    """
    return {
        'NIR': tc_no_input_recover,
        'NMR': tc_no_match_recover,
        'NIF': tc_no_input_3_fail,
        'NMF': tc_no_match_3_fail,
        'NINMF': tc_ni_nm_3_fail,
        'CNIR': tc_confirm_no_input_recover,
        'CNMR': tc_confirm_no_match_recover,
        'CNIF': tc_confirm_no_input_3_fail,
        'CNMF': tc_confirm_no_match_3_fail,
        'CNINMF': tc_confirm_ni_nm_3_fail,
    }.get(key, tc_no_input_recover)


def get_negative_tc_title(key):
    return {
        'NIR': 'No Input & Recover',
        'NMR': 'No Match & Recover',
        'NIF': 'No Input 3 Times Fail',
        'NMF': 'No Match 3 Times Fail',
        'NINMF': 'No Input or No Match 3 Times Fail',
        'CNIR': 'Confirm No Input & Recover',
        'CNMR': 'Confirm No Match & Recover',
        'CNIF': 'Confirm No Input 3 Times Fail',
        'CNMF': 'Confirm No Match 3 Times Fail',
        'CNINMF': 'Confirm No Input or No Match 3 Times Fail',
    }.get(key, 'No Input & Recover')


def negative_testcase_generation(data, path_data, title, node):
    """
    Generate negative TestCases of 5 scenarios
    :param data: Test Steps of current TestCase
    :param path_data: route path of current TestCase
    :param title: title of current TestCase
    :return:
    """
    if node.properties[NON_STANDARD_FAIL_KEY] == 'on':
        for key in NEGATIVE_TESTS_LIST:
            _title = title + ', ' + get_negative_tc_title(key)
            data.append({
                'tcs_cannot_route': 'This test cannot be routed, Non standard fail behavior',
                'title': _title
            })
    else:
        for key in NEGATIVE_TESTS_LIST:
            _title = title + ', ' + get_negative_tc_title(key)
            negative_tc_steps = get_negative_tc_steps(key)(node)

            if not negative_tc_steps[0][TR_CONTENT]:
                data.append({
                    'tcs_cannot_route': negative_tc_steps[0][TR_EXPECTED],
                    'title': _title
                })
            else:
                tc_steps = path_data['tc_steps'] + negative_tc_steps
                data.append({
                    'pre_conditions': path_data['pre_conditions'],
                    'tc_steps': tc_steps,
                    'title': _title
                })


def random_combination(random_size=None):
    """
    Generate random combination of pool
    :return:
    """
    pool = ['NI', 'NM']
    if not random_size:
        random_size = 3
    pool_size = len(pool) - 1
    data = []
    flag = True

    while flag:
        for i in range(random_size):
            index = random.randint(0, pool_size)
            data.append(pool[index])

        if not check_identical(data):
            flag = False
        else:
            data = []

    # print(data)
    return data


def check_identical(data):
    """
    Check elements of list are identical, since 3 NoInputs and 3 NoMatch are covered
    :param data: list of three elements
    :return: True or False
    """
    if data.count(data[0]) == len(data):
        return True
    else:
        return False


def get_no_match_content(node):
    """
    Get a no match content from valid input for NoMatch input
    :param node: current Node
    :return:
    """
    valid_data = []
    for edge in node.leaving_edges:
        if edge.type.name == EDGE_DTMF_NAME and not edge.properties[MP_NC] == 'on':
            valid_data.append(edge.properties[EDGE_PRESS_NAME])
        elif edge.type.name == EDGE_SPEECH_NAME and not edge.properties[MP_NC] == 'on':
            valid_data.append(edge.properties[EDGE_SAY_NAME])

        # Search all following DataQueries node connected to current node
        valid_data += following_dataqueries_node_valid_data(node=edge.to_node,
                                                            subkey=node.properties[MP_OUTPUTS])

    data = generate_no_match_value(valid_data)

    return data


def following_dataqueries_node_valid_data(node, subkey):
    """
    Search all following DataQueries node connected to current node
    :param node:
    :param subkey:
    :return:
    """
    data = []
    if node.type.name in NODE_DATA_NAME:
        for item in node.properties[EDGE_INPUTDATA_NAME]:
            # print(item['Inputs'], node.properties[MP_OUTPUTS])
            try:
                data.append(item[NODE_DATA_INPUTS][subkey])
            except KeyError:
                pass

    for edge in node.leaving_edges:
        data += following_dataqueries_node_valid_data(edge.to_node, subkey)

    return data


def generate_no_match_value(values):
    """
    Generate a random 1 digit number which is different from the number in values
    :param values: list of numbers
    :return:
    """
    data = 'press '
    flag = True

    while flag:
        tmp = str(random.randint(1, 9))
        if tmp not in values:
            data += tmp
            flag = False

    return data


def search_node_name_inside_project(project, node_name):
    """
    Search node name of OnFailGoTo is a valid node name
    :param project:
    :param node_name:
    :return:
    """
    flag = False
    for node in project.nodes:
        if node.name == node_name:
            flag = True
            break

    return flag


def rejected_testcase_generation(data, path_data, title, node):
    """
    Generate rejected TestCase for MenuPromptWithConfirmation Node
    :param data: Output TestCases
    :param path_data: test steps of current TestCase
    :param title: title of current TestCase
    :param node: MenuPromptWithConfirmation Node as last node of current path
    :return: updated param data
    """
    tc_title = title + ', ' + 'Confirm Rejected'

    if node.properties[NON_STANDARD_FAIL_KEY] == 'on':
        data.append({
            'tcs_cannot_route': TESTCASE_NOT_ROUTE_MESSAGE + ', Non standard fail behaviory',
            'title': tc_title
        })
    else:
        if node.properties[ON_FAIL_GO_TO_KEY] == '':
            data.append({
                'tcs_cannot_route': TESTCASE_NOT_ROUTE_MESSAGE + ', OnFailGoTo empty',
                'title': tc_title
            })
        else:
            if not search_node_name_inside_project(node.module.project, node.properties[ON_FAIL_GO_TO_KEY]):
                data.append({
                    'tcs_cannot_route': TESTCASE_NOT_ROUTE_MESSAGE + ', OnFailGoTo node name invalid',
                    'title': tc_title
                })
            else:
                contents = get_mpc_valid_input(node)

                rejected_steps = [
                    {
                        TR_CONTENT: contents,
                        TR_EXPECTED: "{0}: {1}".format(node.name, node.properties[MP_CVER])
                    },
                    {
                        TR_CONTENT: 'press 2',  # rejected confirm
                        TR_EXPECTED: node.properties[MP_VER]
                    }
                ]

                data.append({
                    'pre_conditions': path_data['pre_conditions'],
                    'tc_steps': path_data['tc_steps'] + rejected_steps,
                    'title': tc_title
                })


def get_mpc_valid_input(node):
    """
    Get valid input of MenuPromptWithConfirmation Node from followed date edge
    :param node: current Node
    :return:
    """
    valid_data = []
    for edge in node.leaving_edges:
        if edge.type.name == EDGE_DTMF_NAME and not edge.properties[MP_NC] == 'on':
            valid_data.append({
                EDGE_PRESS_NAME: edge.properties[EDGE_PRESS_NAME]
            })
        elif edge.type.name == EDGE_SPEECH_NAME and not edge.properties[MP_NC] == 'on':
            valid_data.append({
                EDGE_SAY_NAME: edge.properties[EDGE_SAY_NAME]
            })
        elif edge.type.name == EDGE_DATA_NAME:
            valid_data.append(edge.properties[EDGE_OUTPUTDATA_NAME][MP_OUTPUTS])

    if valid_data:
        try:
            contents = 'press '
            for k in valid_data[0]:
                contents += k + ':' + valid_data[0][k] + ', '
        except TypeError:
            contents = 'TypeError'
    else:
        contents = 'No valid inputs'

    return contents
