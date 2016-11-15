import random


NEGATIVE_TESTS_LIST = {
    'NIR': 'No Input & Recover',
    'NMR': 'No Match & Recover',
    'NIF': 'No Input 3 times Fail',
    'NMF': 'No Match 3 times Fail',
    'NINMF': 'No Input or No Match 3 times Fail'
}


def tc_no_input_recover(step):
    data = [
        {
            'content': 'No input',
            'expected': step['expected']
        }
    ]

    return data


def tc_no_match_recover(step):
    data = [
        {
            'content': 'No match',
            'expected': step['expected']
        }
    ]

    return data


def tc_no_input_3_fail(step=None):
    data = []
    for i in range(2):
        data.append({
            'content': 'No Input',
            'expected': step['expected']
        })
    data.append({
        'content': 'No Input',
        'expected': 'Test Fail'
    })

    return data


def tc_no_match_3_fail(step=None):
    data = []
    for i in range(2):
        data.append({
            'content': 'No Match',
            'expected': step['expected']
        })
    data.append({
        'content': 'No Match',
        'expected': 'Test Fail'
    })

    return data


def tc_ni_nm_3_fail(step=None):
    data = []
    combinations = random_combination()
    for i in range(2):
        data.append({
            'content': combinations[i],
            'expected': step['expected']
        })
    data.append({
        'content': combinations[2],
        'expected': 'Test Fail'
    })

    return data


def get_negative_steps(var):
    return {
        'NIR': tc_no_input_recover,
        'NMR': tc_no_match_recover,
        'NIF': tc_no_input_3_fail,
        'NMF': tc_no_match_3_fail,
        'NINMF': tc_ni_nm_3_fail
    }.get(var, tc_no_input_recover)


def negative_testcase_generation(data, path_data, title):
    for key in NEGATIVE_TESTS_LIST:
        _title = title + ', ' + NEGATIVE_TESTS_LIST[key]
        tc_steps = path_data['tc_steps'] + get_negative_steps(key)(path_data['tc_steps'][-1])
        data.append({
            'pre_conditions': path_data['pre_conditions'],
            'tc_steps': tc_steps,
            'title': _title
        })


def random_combination():
    pool = ['No Input', 'No Match']
    size = len(pool) - 1
    data = []

    for i in range(3):
        index = random.randint(0, size)
        data.append(pool[index])

    return data


