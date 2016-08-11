from testrail import APIClient
from mdta.apps.graphs.models import Node, Edge
from mdta.apps.projects.models import Project, TestRailConfiguration


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


def get_projects_from_testrail(instance):
    client = APIClient(instance.host)
    client.user = instance.username
    client.password = instance.password

    return client.send_get('get_projects')


def get_paths_through_all_edges(edges):
    """
    Get all paths through all edges
    :param edges:
    :param data:
    :return:
    """
    data = []
    for edge in edges:
        # print(edge.id)
        path = routing_test(edge)
        if path:
            tcs = []
            for index, step in enumerate(path, start=1):
                if isinstance(step, Node):
                    verify_current_node(step, tcs, index)
                if isinstance(step, Edge):
                    traverse(step, tcs, index)

            data.append(tcs)

    # return check_subpath_in_all(data)
    return data


def routing_test(edge):
    """
    Routing path to current Edge, edge.from_node
    :param edge:
    :return:
    """
    visited_nodes = [edge.to_node]  # Visited nodes for the path to this Edge

    data = []

    route_to(edge.from_node, data, visited_nodes)

    if data:
        data.append(edge)
        data.append(edge.to_node)

    # print(data)
    return data


def route_to(node, data, visited_nodes):
    """
    Routing path to current Node
    :param node:
    :param data:
    :return:
    """
    path = []
    visited_nodes.append(node)

    breadth_first_search(node, path, visited_nodes)

    data += path


def breadth_first_search(node, path, visited_nodes):
    """
    Search a path from Start node(type='Start') to current Node
    Breadh
    :param node:
    :return:
    """

    start_node_found_outside = False  # flag to find Start Node outside

    if node.type.name == 'Start':
        path.append(node)
    else:
        # edges = Edge.objects.filter(to_node=node)
        edges = node.arriving_edges
        if edges.count() > 0:
            start_node_found = False  # flag to find Start Node in current search
            for edge in edges:
                if edge.from_node not in visited_nodes or edge.from_node.type.name == 'Start':  # if Node is not visited or Node is Start
                    if edge.from_node != edge.to_node:
                        if edge.from_node.type.name != 'Start':
                            if edge.from_node.arriving_edges.count() > 0:
                                start_node_found_outside = True
                                breadth_first_search(edge.from_node, path, visited_nodes)
                        else:
                            start_node_found = True
                            path.append(edge.from_node)

                        if start_node_found or start_node_found_outside:  # if found Start Node, add Edge
                            path.append(edge)
                            path.append(node)

                    if start_node_found:  # if found Start Node, break out of for loop
                        break
            if not start_node_found:  # if Not found Start Node, variable Path=[]
                path = []
        else:  # if No Arriving Edges, variable Path=[]
            path = []

    if start_node_found_outside:
        path.append(node)

    # print('path: ', node.name,  path)


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
