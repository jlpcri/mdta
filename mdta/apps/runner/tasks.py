import json
import time

import requests

from mdta.celery_module import app
from mdta.apps.runner.models import TestRun, AutomatedTestCase
from mdta.apps.testcases.testrail import APIClient
from mdta.apps.projects.models import TestRailInstance


@app.task
def poll_result_loop(test_run_id):
    test_run = TestRun.objects.get(pk=test_run_id)
    test_cases = AutomatedTestCase.objects.filter(test_run=test_run)
    if all([c.status != AutomatedTestCase.INCOMPLETE for c in test_cases]):
        return
    poll_result.delay(test_run_id)
    time.sleep(1)
    poll_result_loop.delay(test_run_id)

@app.task
def poll_result(test_run_id):
    test_run = TestRun.objects.get(pk=test_run_id)
    status = test_run.get_current_hat_results()
    tri = TestRailInstance.objects.first()
    client = APIClient(tri.host)
    client.user = tri.username
    client.password = tri.password
    jsonList = []
    for call in status['calls']:
        try:
            tc_id = call['options']['id'].split(':')[0]
        except TypeError:
            # Super fragile JSON correction method.
            options_text = call['options'].replace("'everything': '", '"everything": "')
            options_text = options_text.replace("', 'id': '", '", "id": "')
            options_text = options_text.replace("', 'id':", '", "id":')
            options_text = options_text.replace("'}", '"}')
            print(options_text)
            options_json = json.loads(options_text)
            tc_id = options_json['id'].split(':')[0]

        atc = AutomatedTestCase.objects.get(test_run=test_run, testrail_case_id=tc_id)
        if call['status'].upper() == 'PASS':
            atc.status = AutomatedTestCase.PASS
            response = client.send_post('add_result_for_case/{0}/{1}'.format(test_run.testrail_test_run, tc_id),
                                       {'status_id': 1})
            print(response)
            jsonList.append(response)
            for data in jsonList:
                atc.tr_test_id = data['test_id']
                atc.save()
        else:
            atc.status = AutomatedTestCase.FAIL
            atc.failure_reason = call['err_str']
            response = client.send_post('add_result_for_case/{0}/{1}'.format(test_run.testrail_test_run, tc_id),
                             {'status_id': 5, 'defects': call['err_str']})
            print(response)
            jsonList.append(response)
            for data in jsonList:
                atc.tr_test_id = data['test_id']
                atc.save()

        atc.call_id = call['callseq']
        atc.save()
    if status['complete']:
        remaining_test_cases = test_run.automatedtestcase_set.filter(status=AutomatedTestCase.INCOMPLETE)

        for case in remaining_test_cases:
            case.status = AutomatedTestCase.FAIL
            case.failure_reason = 'MDTA error - could not find test result in completed run'
            case.save()
            client.send_post('add_result_for_case/{0}/{1}'.format(test_run.testrail_test_run, tc_id),
                             {'status_id': 4, 'comment': 'MDTA error - could not find result'})

        client.send_post('close_run/{0}'.format(test_run.testrail_test_run), {})
