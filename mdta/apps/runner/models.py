import json

import requests

from django.db import models
from django.utils.datetime_safe import time
from django.core.validators import URLValidator


class TestServers(models.Model):
    server = models.TextField()
    server_url = models.TextField(default='')
    name = models.TextField(unique=True)

    def __str__(self):
        return '{0}: {1}'.format(self.server, self.name)


class TestRun(models.Model):
    hat_run_id = models.IntegerField()
    hat_server = models.ForeignKey('TestServers')
    testrail_project_id = models.IntegerField()
    testrail_suite_id = models.IntegerField()
    testrail_test_run = models.IntegerField()
    project = models.ForeignKey('projects.Project')

    def get_current_hat_results(self):
        response = requests.get(self.hat_server.server + 'api/check_run/?runid=' + str(self.hat_run_id))
        return json.loads(response.text)


class AutomatedTestCase(models.Model):
    INCOMPLETE = 1
    PASS = 2
    FAIL = 3
    STATUS_CHOICES = (
        (INCOMPLETE, 'Incomplete'),
        (PASS, 'Pass'),
        (FAIL, 'Fail'),
    )
    test_run = models.ForeignKey('TestRun')
    testrail_case_id = models.IntegerField()
    status = models.IntegerField(choices=STATUS_CHOICES, default=INCOMPLETE)
    failure_reason = models.TextField(default='')
    call_id = models.TextField(default='')
    tr_test_id = models.TextField(default='')
    case_title = models.TextField(default='')
