from django.db import models
from django.utils.datetime_safe import time

class TestServers(models.Model):
    server = models.TextField()
    name = models.TextField(unique=True)

class TestRun(models.Model):
    hat_run_id = models.IntegerField()
    hat_server = models.ForeignKey('TestServers')
    testrail_project_id = models.IntegerField()
    testrail_suite_id = models.IntegerField()
    testrail_test_run = models.IntegerField()
    project = models.ForeignKey('projects.Project')

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
