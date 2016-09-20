import ast
from django.shortcuts import get_object_or_404

from mdta.apps.graphs.models import Node, Edge
from mdta.apps.projects.models import Project, TestRailConfiguration, Module
from mdta.apps.testcases.testrail import APIClient, APIError

START_NODE_NAME = ['Start', 'TestHeader Start']


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

    if len(modules) > 0 and modules[0].project.test_header:
        th_module = modules[0].project.test_header
    else:
        th_module = None

    for module in modules:
        data = get_paths_through_all_edges(module.edges_all, th_module)

        test_suites.append({
            'module': module.name,
            'data': data
        })

    return test_suites


def get_paths_through_all_edges(edges, th_module=None):
    """
    Get all paths through all edges
    :param edges:
    :return:
    """
    th_paths = get_paths_from_test_header(th_module)
    # print(th_paths)

    data = []
    if th_paths:
        for th_path in th_paths:
            for edge in edges:
                # print(edge.id)
                path = routing_path_to_edge(edge)
                if path:
                    tcs = []
                    pre_condition = []
                    # for index, step in enumerate(path, start=1):
                    if isinstance(path[0], Node) and path[0].type.name in START_NODE_NAME:
                        for index, step in enumerate(path):
                            if index == 0:
                                traverse_node(step, tcs)
                                if th_path:
                                    for th_index, th_step in enumerate(th_path):
                                        if th_index == 0:
                                            traverse_node(th_step, tcs)
                                        else:
                                            if isinstance(th_step, Node):
                                                traverse_node(th_step, tcs, th_path[th_index - 1])
                                            elif isinstance(th_step, Edge):
                                                traverse_edge(th_step, tcs)
                            else:
                                if isinstance(step, Node):
                                    traverse_node(step, tcs, path[index - 1])
                                elif isinstance(step, Edge):
                                    if step.type.name == 'PreCondition':
                                        update_testcase_precondition(step, pre_condition)
                                    traverse_edge(step, tcs)

                        data.append({
                            'pre_condition': pre_condition,
                            'tc_steps': tcs,
                            'title': 'Route from \'' + edge.from_node.name + '\' to \'' + edge.to_node.name + '\''
                        })
    else:
        for edge in edges:
            # print(edge.id)
            path = routing_path_to_edge(edge)
            if path:
                tcs = []
                pre_condition = []
                # for index, step in enumerate(path, start=1):
                if isinstance(path[0], Node) and path[0].type.name in START_NODE_NAME:
                    for index, step in enumerate(path):
                        if index == 0:
                            traverse_node(step, tcs)
                        else:
                            if isinstance(step, Node):
                                traverse_node(step, tcs, path[index - 1])
                            elif isinstance(step, Edge):
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

    if node.type.name in START_NODE_NAME:
        path.append(node)
    else:
        edges = node.arriving_edges
        if edges.count() == 1:
            edge = edges[0]
        elif edges.count() > 1:
            for tmp_edge in edges:
                if tmp_edge.type.name == 'Connector':
                    edge = tmp_edge
                    break
            else:
                edge = edges[0]
        else:
            edge = None

        if edge:
            start_node_found = False  # flag to find Start Node in current search
            if edge.from_node not in visited_nodes or edge.from_node.type.name in START_NODE_NAME:  # if Node is not visited or Node is Start
                if edge.from_node != edge.to_node:
                    if edge.from_node.type.name not in START_NODE_NAME:
                        if edge.from_node.arriving_edges.count() > 0:
                            start_node_found_outside = True
                            path += breadth_first_search(edge.from_node, visited_nodes)
                    else:
                        start_node_found = True
                        path.append(edge.from_node)

                    if start_node_found or start_node_found_outside:  # if found Start Node, add Edge
                        path.append(edge)
                        path.append(node)

                # if start_node_found:  # if found Start Node, break out of for loop
                #     break

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
    if node.type.name == START_NODE_NAME[0]:  # Start with Dial Number
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
        if key == 'InputData':
            try:
                for ele in item.properties[key]:
                    data += 'Inputs: ' + str(ele['Inputs']) + ', Outputs: ' + str(ele['Outputs']) + '; '
            except (KeyError, TypeError):
                data += key
        elif key == 'OutputData':
            try:
                data += str(item.properties[key][item.type.subkeys_data_name])
            except KeyError:
                data += key
        else:
            try:
                data += key + ': ' + item.properties[key] + ', '
            except (KeyError, TypeError):
                data += key

    return data


def update_testcase_precondition(edge, pre_condition):
    data = ''
    try:
        for subkey in edge.properties[edge.type.keys_data_name]:
            tmp = edge.properties[edge.type.keys_data_name][subkey]
            tmp = ast.literal_eval(tmp)
            for idx, tmp_key in enumerate(tmp):
                if idx == len(tmp) - 1:
                    data += tmp_key + ': ' + tmp[tmp_key]
                else:
                    data += tmp_key + ': ' + tmp[tmp_key] + ', '
            # data += edge.properties[edge.type.keys_data_name][subkey]

        pre_condition.append(data)
    except (KeyError, TypeError) as e:
        print('PreCondition update error: ', e)
        pass

# --------------- Routing Project/Module Graph End ---------------


# --------------- Routing Test Header Graph End ---------------
def get_paths_from_test_header(th_module):
    data = []
    if th_module:
        try:
            end_node = Node.objects.get(module=th_module, type__name='TestHeader End')
            for edge in end_node.arriving_edges:
                path = routing_path_to_edge(edge)
                data.append(path)
        except Exception as e:
            print('TestHeader error: ', e)
            pass

    return data
# --------------- Routing Test Header Graph End ---------------


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
        print('Add TestCase to Section error: ', e)


# --------------- TestRail End ---------------


# --------------- Hat Scripts Start ---------------
def create_hat_scripts_for_project_or_module(project_id=None, module_id=None):
    """
    Create Hat Scripts per Project
    :param project_id:
    :return:
    """

    if project_id:
        project = get_object_or_404(Project, pk=project_id)
        tcs = project.testcaseresults_set.latest('updated').results
        for tc in tcs:
            print(tc['module'])
            if tc['data']:
                for index, item in enumerate(tc['data']):
                    create_hat_scripts_per_tc(index, item['pre_condition'], item['tc_steps'])
    elif module_id:
        module = get_object_or_404(Module, pk=module_id)
        tmp_tcs = module.project.testcaseresults_set.latest('updated').results
        tcs = [(item for item in tmp_tcs if item['module'] == module.name).__next__()]
        for tc in tcs:
            print(tc['module'])
            if tc['data']:
                for index, item in enumerate(tc['data']):
                    create_hat_scripts_per_tc(index, item['pre_condition'], item['tc_steps'])


def create_hat_scripts_per_tc(index, pre_condition, steps):
    print(index, '\nPreCondition: ', pre_condition)
    for step in steps:
        print(step)


# --------------- Hat Scripts End ---------------
