import random


NEGATIVE_TESTS_LIST = ['NIR', 'NMR', 'NIF', 'NMF', 'NINMF']


def tc_no_input_recover(step, repeat=None, node=None):
    """
    Test step of No Input and recover to self
    :param step: self step
    :return:
    """
    data = [
        {
            'content': 'wait',
            'expected': node.name + 'NI1: ' + node.properties['NoInput_1']
        }
    ]

    return data


def tc_no_match_recover(step, repeat=None, node=None):
    """
    Test step of No Match and recover to self
    :param step: self step
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


def tc_no_input_3_fail(step=None, repeat=None, node=None):
    """
    Test step of 3 times No Input then Fail
    :param step: self step
    :return:
    """
    data = []
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
        'expected': 'Test fail, route to: ' + node.properties['OnFailGoTo']
    })

    return data


def tc_no_match_3_fail(step=None, repeat=None, node=None):
    """
    Test step of 3 times No Match then Fail
    :param step: self step
    :return:
    """
    data = []
    for i in range(repeat - 1):
        data.append({
            'content': 'No Match',
            'expected': step['expected']
        })
    data.append({
        'content': 'No Match',
        'expected': 'Test Fail'
    })

    return data


def tc_ni_nm_3_fail(step=None, repeat=None, node=None):
    """
    Test step of 3 times 'No Input' or 'No Match' then Fail
    :param step: self step
    :return:
    """
    data = []
    combinations = random_combination(repeat)
    for i in range(repeat - 1):
        data.append({
            'content': combinations[i],
            'expected': step['expected']
        })
    data.append({
        'content': combinations[repeat - 1],
        'expected': 'Test Fail'
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


def get_negative_tc_title(key, repeat):
    return {
        'NIR': 'No Input & Recover',
        'NMR': 'No Match & Recover',
        'NIF': 'No Input {0} Times Fail'.format(repeat),
        'NMF': 'No Match {0} Times Fail'.format(repeat),
        'NINMF': 'No Input or No Match {0} Times Fail'.format(repeat)
    }.get(key, 'No Input & Recover')


def negative_testcase_generation(data, path_data, title, node):
    """
    Generate negative TestCases of 5 scenarios
    :param data: Test Steps of current TestCase
    :param path_data: route path of current TestCase
    :param title: title of current TestCase
    :return:
    """
    repeat = 3
    for key in NEGATIVE_TESTS_LIST:
        _title = title + ', ' + get_negative_tc_title(key, repeat)
        tc_steps = path_data['tc_steps'] + get_negative_tc_steps(key)(path_data['tc_steps'][-1], repeat, node)
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
    pool = ['No Input', 'No Match']
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
    Check elements of list are identical
    :param data:
    :return:
    """
    if data.count(data[0]) == len(data):
        return True
    else:
        return False


def get_no_match_content(node):
    valid_data = []
    for edge in node.leaving_edges:
        if edge.type.name == 'DTMF':
            valid_data.append(edge.properties['Press'])
        elif edge.type.name == 'Speech':
            valid_data.append(edge.properties['Say'])

    data = generate_no_match_value(valid_data)

    return data


def generate_no_match_value(values):
    data = 'press '
    flag = True

    while flag:
        tmp = random.randint(0, 9)
        if tmp not in values:
            data += str(tmp)
            flag = False

    return data
