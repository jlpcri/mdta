from django.db import models
from django.utils.datetime_safe import time


class TestServers(models.Model):
    server = models.TextField()
    name = models.TextField(unique=True)


class TestRun(models.Model):
    hat_run_id = models.IntegerField()
    testrail_project_id = models.IntegerField()
    testrail_suite_id = models.IntegerField()
    project = models.ForeignKey('projects.Project')