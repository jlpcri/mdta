from testrail import APIClient, APIError
from mdta.apps.graphs.models import Node, Edge
from mdta.apps.projects.models import Project, TestRailConfiguration

START_NODE_NAME = 'Start'


def context_testcases():
    """
    Retrieve context for tab TestCases
    :return:
    """
    context = {
        'projects': Project.objects.all(),
        'testrails': TestRailConfiguration.objects.all(),
    }

    return context


# --------------- Routing Project/Module Graph Start ---------------
def create_routing_test_suite(project=None, modules=None):
    """
    Create routing paths for project.modules lists or module lists
    :param project:
    :param modules:
    :return:
    """
    data = []

    if project:
        data = create_routing_test_suite_module(project.modules)
    elif modules:
        data = create_routing_test_suite_module(modules)

    return data


def create_routing_test_suite_module(modules):
    """
    Create routing paths for list of modules
    :param modules:
    :return:
    """
    test_suites = []

    for module in modules:
        data = get_paths_through_all_edges(module.edges_all)

        test_suites.append({
            'module': module.name,
            'data': data
        })

    return test_suites


def get_paths_through_all_edges(edges):
    """
    Get all paths through all edges
    :param edges:
    :return:
    """
    data = []
    for edge in edges:
        # print(edge.id)
        path = routing_path_to_edge(edge)
        if path:
            tcs = []
            pre_condition = []
            # for index, step in enumerate(path, start=1):
            if isinstance(path[0], Node) and path[0].type.name == START_NODE_NAME:
                for index, step in enumerate(path):
                    if isinstance(step, Node):
                        if index > 1:
                            traverse_node(step, tcs, path[index-1])
                        else:
                            traverse_node(step, tcs)
                    if isinstance(step, Edge):
                        if step.type.name == 'PreCondition':
                            update_testcase_precondition(step, pre_condition)
                        traverse_edge(step, tcs)

                data.append({
                    'pre_condition': pre_condition,
                    'tc_steps': tcs,
                    'title': 'Route from \'' + edge.from_node.name + '\' to \'' + edge.to_node.name + '\''
                })
    # return check_subpath_in_all(data)
    return data


def routing_path_to_edge(edge):
    """
    Routing path to current Edge, edge.from_node
    :param edge:
    :return:
    """
    visited_nodes = [edge.to_node]  # Visited nodes for the path to this Edge

    data = routing_path_to_node(edge.from_node, visited_nodes)

    if data:
        data.append(edge)
        data.append(edge.to_node)

    # print(data)
    return data


def routing_path_to_node(node, visited_nodes):
    """
    Routing path to current Node
    :param node:
    :param data:
    :return:
    """

    visited_nodes.append(node)

    path = breadth_first_search(node, visited_nodes)

    # print(path)
    return path


def breadth_first_search(node, visited_nodes):
    """
    Search a path from Start node(type='Start') to current Node
    Breadth
    :param node:
    :return:
    """

    path = []
    start_node_found_outside = False  # flag to find Start Node outside

    if node.type.name == START_NODE_NAME:
        path.append(node)
    else:
        edges = node.arriving_edges
        if edges.count() > 0:
            start_node_found = False  # flag to find Start Node in current search
            for edge in edges:
                if edge.from_node not in visited_nodes or edge.from_node.type.name == START_NODE_NAME:  # if Node is not visited or Node is Start
                    if edge.from_node != edge.to_node:
                        if edge.from_node.type.name != START_NODE_NAME:
                            if edge.from_node.arriving_edges.count() > 0:
                                start_node_found_outside = True
                                path += breadth_first_search(edge.from_node, visited_nodes)
                        else:
                            start_node_found = True
                            path.append(edge.from_node)

                        if start_node_found or start_node_found_outside:  # if found Start Node, add Edge
                            path.append(edge)
                            path.append(node)

                    if start_node_found:  # if found Start Node, break out of for loop
                        break

    # print('path: ',  path)
    return path


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


def traverse_node(node, tcs, preceding_edge=None):
    """
    Traverse Node based on node type
    :param node:
    :param tcs:
    :return:
    """
    if node.type.name == START_NODE_NAME:
        add_step(node_start(node), tcs)
    elif node.type.name in ['Menu Prompt', 'Menu Prompt with Confirmation', 'Play Prompt']:
        add_step(node_prompt(node, preceding_edge), tcs)
    else:
        add_step(node_check_holly_log(node), tcs)


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


def node_check_holly_log(node):
    if node.properties:
        data = {
            'content': 'Node - ' + node.name + ', ' + get_item_properties(node)
        }
    else:
        data = {
            'content': 'Node - ' + node.name
        }

    return data


def traverse_edge(edge, tcs):
    """
    Traverse Edge based on edge type
    :param edge:
    :param tcs:
    :return:
    """
    # if edge.type.name == 'DTMF':
    #     add_step(edge_dtmf_dial(edge), tcs)
    # elif edge.type.name == 'Speech':
    #     add_step(edge_speech_say(edge), tcs)
    if edge.type.name == 'Data':
        add_step(edge_alter_data_requirement(edge), tcs)
    elif edge.type.name == 'PreCondition':
        add_step(edge_precondition(edge), tcs)


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


def edge_dtmf_dial(edge):
    return {
        'content': 'DTMF Dial - ' + get_item_properties(edge)
    }


def edge_speech_say(edge):
    return {
        'content': 'Speech Say - ' + get_item_properties(edge)
    }


def edge_alter_data_requirement(edge):
    return {
        'content': 'Alter Data Requirement - ' + get_item_properties(edge)
    }


def edge_precondition(edge):
    return {
        'content': 'PreCondition - ' + get_item_properties(edge)
    }


def get_item_properties(item):
    data = ''
    for key in item.properties:
        if key == item.type.keys_data_name:
            for subkey in item.properties[key]:
                data += subkey + ': ' + item.properties[key][subkey] + ', '
        else:
            data += key + ': ' + item.properties[key] + ', '

    return data


def update_testcase_precondition(edge, pre_condition):
    data = []
    for key in edge.properties[edge.type.keys_data_name]:
        data.append(key + ': ' + edge.properties[edge.type.keys_data_name][key])

    pre_condition.append(data)

# --------------- Routing Project/Module Graph End ---------------


# --------------- TestRail Start ---------------
def get_projects_from_testrail(instance):
    """
    Get Projects from TestRail to help adding TestRail Configuration
    :param instance:
    :return:
    """
    client = APIClient(instance.host)
    client.user = instance.username
    client.password = instance.password

    return client.send_get('get_projects')


def add_testsuite_to_project(client, project_id, suite_name):
    data = {
        'name': suite_name,
        'description': ''
    }

    try:
        suite = client.send_post('add_suite/' + project_id, data)
        return suite
    except APIError as e:
        print('Add Suite Error: ', e)
        return None


def add_section_to_testsuite(client, project_id, suite_id, section_name):
    data = {
        'suite_id': suite_id,
        'name': section_name
    }

    section = client.send_post('add_section/' + project_id, data)

    return str(section['id'])


def remove_section_from_testsuite(client, section_id):
    client.send_post('delete_section/' + section_id, None)


def add_testcase_to_section(client, section_id, data):
    try:
        for each_tc in data:
            custom_preconds = ''
            for pre_cond in each_tc['pre_condition']:
                custom_preconds += ', '.join(pre_cond) + '; '
            tc_data = {
                'title': each_tc['title'],
                'custom_preconds': custom_preconds,
                'custom_steps_seperated': each_tc['tc_steps']
            }
            client.send_post('add_case/' + section_id, tc_data)
    except APIError as e:
        print('TestCase: ', e)


# --------------- TestRail End ---------------
