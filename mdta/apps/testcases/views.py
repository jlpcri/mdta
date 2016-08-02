from django.shortcuts import redirect, get_object_or_404, render

from mdta.apps.projects.models import Project, Module
from mdta.apps.graphs.models import Node, Edge
from mdta.apps.projects.utils import context_projects
from .utils import traverse, add_step, verify_current_node


def create_testcases(request, object_id):
    """
    Create TestCases per project/module
    :param request:
    :param object_id: project_id/module_id
    :return:
    """

    testcases = []
    level = request.GET.get('level', '')
    if level == 'project':
        project = get_object_or_404(Project, pk=object_id)
        testcases = create_routing_test_suite(project)
    elif level == 'module':
        module = get_object_or_404(Module, pk=object_id)
        testcases = create_routing_test_suite(modules=[module])

    context = context_projects()
    context['testcases'] = testcases
    # print(testcases)

    return render(request, 'projects/projects.html', context)


def create_routing_test_suite(project=None, modules=None):
    """
    Create routing test suite for Project/Module lists
    :param project:
    :param modules:
    :return:
    """
    data = []

    if project:
        # print(project.modules)
        data = create_routing_test_suite_module(project.modules)
    elif modules:
        data = create_routing_test_suite_module(modules)

    return data


def create_routing_test_suite_module(modules):
    test_suites = []

    for module in modules:
        data = []
        for edge in module.edges_all:
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

        test_suites.append({
            'module': module.name,
            'data': data
        })

    return test_suites


def routing_test(edge):
    """
    Routing tests to current Edge
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
