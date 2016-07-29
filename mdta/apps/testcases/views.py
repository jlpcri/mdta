from django.shortcuts import redirect, get_object_or_404

from mdta.apps.projects.models import Project, Module
from mdta.apps.graphs.models import Node, Edge


def create_testcases(request, object_id):
    """
    Create TestCases per project/module
    :param request:
    :param object_id: project_id/module_id
    :return:
    """

    level = request.GET.get('level', '')
    if level == 'project':
        project = get_object_or_404(Project, pk=object_id)
        create_routing_test_suite(project)
    elif level == 'module':
        module = get_object_or_404(Module, pk=object_id)
        create_routing_test_suite(modules=[module])

    return redirect('projects:projects')


def create_routing_test_suite(project=None, modules=None):
    """
    Create routing test suite for Project/Module lists
    :param project:
    :param modules:
    :return:
    """
    data = []

    if project:
        print(project.name)
    elif modules:
        for module in modules:
            for edge in module.edges_all:
                print(edge.id)
                data.append(routing_test(edge))


def routing_test(edge):
    """
    Routing tests to current Edge
    :param edge:
    :return:
    """
    visited_nodes = [edge.to_node]  # Visited nodes for the path to this Edge

    data = []

    route_to(edge.from_node, data, visited_nodes)

    data.append(edge.id)
    data.append(edge.to_node.name)

    print(data)
    return data


def route_to(node, data, visited_nodes):
    """
    Routing tests to current Node
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

    if node.type.name == 'Start':
        path.append(node.name)
    else:
        edges = Edge.objects.filter(to_node=node)
        if edges.count() > 0:
            for edge in edges:
                if edge.from_node not in visited_nodes:
                    if edge.from_node != edge.to_node:
                        if edge.from_node.type.name != 'Start':
                            breadth_first_search(edge.from_node, path, visited_nodes)
                        else:
                            path.append(edge.from_node.name)
                        path.append(edge.id)

    path.append(node.name)

    # print('path: ', node.name,  path)
