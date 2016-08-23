from datetime import datetime
from django.shortcuts import get_object_or_404

from mdta.celery_module import app
from mdta.apps.projects.models import Project
from mdta.apps.testcases.models import TestCaseResults
from mdta.apps.testcases.utils import create_routing_test_suite


@app.task
def create_testcases_celery(project_id):
    """
    Create TestCases per project/module
    :param request:
    :param project_id:
    :return:
    """

    project = get_object_or_404(Project, pk=project_id)
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
        except Exception as e:
            print(str(e))

