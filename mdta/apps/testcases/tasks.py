from datetime import datetime
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from mdta.celery_module import app
from mdta.apps.projects.models import Project
from mdta.apps.testcases.models import TestCaseResults
from mdta.apps.testcases.utils import create_routing_test_suite, add_testsuite_to_project, remove_section_from_testsuite, \
    add_section_to_testsuite, add_testcase_to_section
from mdta.apps.testcases.testrail import APIClient


@app.task(bind=True)
def create_testcases_celery(self, project_id):
    """
    Create TestCases per project/module
    :param request:
    :param project_id:
    :return:
    """

    # self.update_state(state='PROGRESS', meta={'process_percent': 10})
    # sleep(10)

    project = get_object_or_404(Project, pk=project_id)

    edges = project.edges
    for edge in edges:
        edge.celery_visited = True
        edge.save()

    testcases = create_routing_test_suite(project=project)
    tc_results = TestCaseResults.objects.filter(project=project)
    if tc_results.count() > 2:
        tc_latest = project.testcaseresults_set.latest('updated')
        if tc_latest.results == testcases:
            tc_latest.updated = datetime.now()
            tc_latest.save()
        else:

            tc_earliest = project.testcaseresults_set.earliest('updated')
            tc_earliest.results = testcases
            tc_earliest.updated = datetime.now()
            tc_earliest.save()
    else:
        try:
            TestCaseResults.objects.create(
                project=project,
                results=testcases
            )
        except (ValueError, ValidationError) as e:
            print(str(e))
    msg = push_testcases_to_testrail_celery(project.id)

    return msg


@app.task(bind=True)
def push_testcases_to_testrail_celery(self, project_id):
    """
    Push Testcases of project to TestRail
    :param request:
    :param project_id:
    :return:
    """
    project = get_object_or_404(Project, pk=project_id)
    testrail_contents = ''

    try:
        client = APIClient(project.testrail.instance.host)
        client.user = project.testrail.instance.username
        client.password = project.testrail.instance.password
        testrail_contents = client.send_get('get_project/' + project.testrail.project_id)

        tr_suites = client.send_get('get_suites/' + project.testrail.project_id)
        testcases = project.testcaseresults_set.latest('updated').results

        # Find or Create TestSuites in TestRail
        try:
            tr_suite = (suite for suite in tr_suites if suite['name'] == project.version).__next__()
        except StopIteration as e:
            print('Suite: ', e)
            tr_suite = add_testsuite_to_project(client,
                                                project.testrail.project_id,
                                                project.version)
            if not tr_suite:
                raise PermissionError('You are not allowed (Insufficient Permissions)')

        tr_suite_sections = client.send_get('get_sections/' + project.testrail.project_id + '&suite_id=' + str(tr_suite['id']))

        # Find or Create Section of TestSuites
        for item in testcases:

            try:
                section = (section for section in tr_suite_sections if section['name'] == item['module']).__next__()
                remove_section_from_testsuite(client, str(section['id']))

                section_id = add_section_to_testsuite(client,
                                                      project.testrail.project_id,
                                                      tr_suite['id'],
                                                      item['module'])
                add_testcase_to_section(client, section_id, item['data'])

            except StopIteration as e:
                print('Section: ', e)
                section_id = add_section_to_testsuite(client,
                                                      project.testrail.project_id,
                                                      tr_suite['id'],
                                                      item['module'])
                add_testcase_to_section(client, section_id, item['data'])

    except AttributeError:
        testrail_contents = {
            'error': 'No TestRail config'
        }

    except (TestCaseResults.DoesNotExist, PermissionError) as e:
        testrail_contents = {
            'error': e
        }
    return testrail_contents

