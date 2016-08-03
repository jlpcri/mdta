def check_subpath_in_all(all_path):
    """
    Find sub paths contained by parent path in all possible paths and remove them
    Use set(a) < set(b) to compare if list_b contains list_a
    :param all_path:
    :return:
    """
    data = []
    length = len(all_path)
    for i in range(length):
        for j in range(i + 1, length):
            if set(all_path[i]) < set(all_path[j]) and not check_path_contains_in_result(all_path[j], data):
                data.append(all_path[j])
            elif set(all_path[i]) > set(all_path[j]) and not check_path_contains_in_result(all_path[i], data):
                data.append(all_path[i])

    # check if first path of all_path is in result
    if length > 0 and not check_path_contains_in_result(all_path[0], data):
        data.append(all_path[0])

    return data


def check_path_contains_in_result(path, result):
    """
    Check current path is covered in result
    :param path:
    :param result:
    :return:
    """
    flag = False
    for i in range(len(result)):
        if set(path) <= set(result[i]):
            flag = True
            break
        else:
            continue

    return flag


def traverse(edge, tcs, index):
    """
    Traverse Edge based on edge type
    :param edge:
    :param tcs:
    :param index:
    :return:
    """
    if edge.type.name == 'DTMF':
        add_step(edge_dtmf_dial(edge), tcs, index)
    elif edge.type.name == 'Speech':
        add_step(edge_speech_say(edge), tcs, index)
    elif edge.type.name == 'Data':
        add_step(edge_alter_data_requirement(edge), tcs, index)


def add_step(step, tcs, index):
    """
    Add step to test cases
    :param step:
    :param tcs:
    :param index:
    :return:
    """
    tcs.append(str(index) + ', ' + step)


def verify_current_node(node, tcs, index):
    """
    Verify current node from holly logs, will do in the future
    :param node:
    :param tcs:
    :param index:
    :return:
    """
    add_step(node_check_holly_log(node), tcs, index)


def node_check_holly_log(node):
    return 'Node - ' + node.name


def edge_dtmf_dial(edge):
    return 'DTMF Dial - ' + get_edge_properties(edge)


def edge_speech_say(edge):
    return 'Speech Say - ' + get_edge_properties(edge)


def edge_alter_data_requirement(edge):
    return 'Alter Data Requirement - ' + get_edge_properties(edge)


def get_edge_properties(edge):
    data = ''
    for key in edge.properties:
        data += edge.properties[key]

    return data
