import random


NEGATIVE_TESTS_LIST = ['NIR', 'NMR', 'NIF', 'NMF', 'NINMF']
ON_FAIL_GO_TO_KEY = 'OnFailGoTo'
NON_STANDARD_FAIL_KEY = 'NonStandardFail'


def tc_no_input_recover(node):
    """
    Test step of No Input and recover to self
    :return:
    """
    data = [
        {
            'content': 'wait',
            'expected': node.name + 'NI1: ' + node.properties['NoInput_1']
        }
    ]

    return data


def tc_no_match_recover(node):
    """
    Test step of No Match and recover to self
    :return:
    """
    no_match_conent = get_no_match_content(node)
    data = [
        {
            'content': no_match_conent,
            'expected': node.name + 'NM1: ' + node.properties['NoMatch_1']
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
            'content': False,
            'expected': 'This test cannot be routed, OnFailGoTo empty'
        })
    elif not search_node_name_inside_project(node.module.project, node.properties[ON_FAIL_GO_TO_KEY]):
        data.append({
            'content': False,
            'expected': 'This test cannot be routed, OnFailGoTo node name invalid'
        })
    else:
        data.append({
            'content': 'wait',
            'expected': node.name + 'NI1: ' + node.properties['NoInput_1']
        })
        data.append({
            'content': 'wait',
            'expected': node.name + 'NI2: ' + node.properties['NoInput_2']
        })
        data.append({
            'content': 'wait',
            'expected': 'Test fail, route to: ' + node.properties[ON_FAIL_GO_TO_KEY]
        })

    return data


def tc_no_match_3_fail(node):
    """
    Test step of 3 times No Match then Fail
    :return:
    """
    data = []

    if node.properties[ON_FAIL_GO_TO_KEY] == '':
        data.append({
            'content': False,
            'expected': 'This test cannot be routed, OnFailGoTo empty'
        })
    elif not search_node_name_inside_project(node.module.project, node.properties[ON_FAIL_GO_TO_KEY]):
        data.append({
            'content': False,
            'expected': 'This test cannot be routed, OnFailGoTo node name invalid'
        })
    else:
        no_match_content = get_no_match_content(node)
        data.append({
            'content': no_match_content,
            'expected': node.name + 'NM1: ' + node.properties['NoMatch_1']
        })

        no_match_content = get_no_match_content(node)
        data.append({
            'content': no_match_content,
            'expected': node.name + 'NM2: ' + node.properties['NoMatch_2']
        })

        no_match_content = get_no_match_content(node)
        data.append({
            'content': no_match_content,
            'expected': 'Test fail, route to: ' + node.properties[ON_FAIL_GO_TO_KEY]
        })

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
            'content': False,
            'expected': 'This test cannot be routed, OnFailGoTo empty'
        })
    elif not search_node_name_inside_project(node.module.project, node.properties[ON_FAIL_GO_TO_KEY]):
        data.append({
            'content': False,
            'expected': 'This test cannot be routed, OnFailGoTo node name invalid'
        })
    else:
        combinations = random_combination(3)
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
                'content': content,
                'expected': expected
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
        'NINMF': tc_ni_nm_3_fail
    }.get(key, tc_no_input_recover)


def get_negative_tc_title(key):
    return {
        'NIR': 'No Input & Recover',
        'NMR': 'No Match & Recover',
        'NIF': 'No Input 3 Times Fail',
        'NMF': 'No Match 3 Times Fail',
        'NINMF': 'No Input or No Match 3 Times Fail'
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

            if not negative_tc_steps[0]['content']:
                data.append({
                    'tcs_cannot_route': negative_tc_steps[0]['expected'],
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
        if edge.type.name == 'DTMF':
            valid_data.append(edge.properties['Press'])
        elif edge.type.name == 'Speech':
            valid_data.append(edge.properties['Say'])

        # Search all following DataQueries node connected to current node
        valid_data += following_dataqueries_node_valid_data(node=edge.to_node,
                                                            subkey=node.properties['Outputs'])

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
    if node.type.name in ['DataQueries Database', 'DataQueries WebService']:
        for item in node.properties['InputData']:
            # print(item['Inputs'], node.properties['Outputs'])
            try:
                data.append(item['Inputs'][subkey])
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
