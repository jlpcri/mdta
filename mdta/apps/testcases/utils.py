
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
