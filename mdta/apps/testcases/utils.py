def check_duplicate_path(all_path):
    data = []
    length = len(all_path)
    for i in range(length):
        if len(data) == 0:
            data.append(all_path[i])
        else:
            for j in range(1, length):
                if set(all_path[i]) < set(all_path[j]) and not check_path_contains_in_result(all_path[j], data):
                    data.append(all_path[j])
                elif set(all_path[i]) > set(all_path[j]) and not check_path_contains_in_result(all_path[i], data):
                    data.append(all_path[i])

    return data


def check_path_contains_in_result(path, result):
    flag = False
    for i in range(len(result)):
        if set(path) <= set(result[i]):
            flag = True
            break
        else:
            continue

    return flag


def traverse(edge, tcs, index):
    if edge.type.name == 'DTMF':
        add_step(edge_dtmf_dial(edge), tcs, index)
    elif edge.type.name == 'Speech':
        add_step(edge_speech_say(edge), tcs, index)
    elif edge.type.name == 'Data':
        add_step(edge_alter_data_requirement(edge), tcs, index)


def add_step(step, tcs, index):
    tcs.append(str(index) + ', ' + step)


def verify_current_node(node, tcs, index):
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
