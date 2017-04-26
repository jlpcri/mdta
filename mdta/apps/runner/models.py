from django.db import models
from django.utils.datetime_safe import time


class TestServer(models.Model):
    host = models.TextField()
    remote_user = models.TextField()
    remote_password = models.TextField()
    name = models.TextField(unique=True)

class TestRun(models.Model):
    hat_run_id = models.IntegerField()
    testrail_project_id = models.IntegerField()
    testrail_suite_id = models.IntegerField()
    project = models.ForeignKey('projects.Project')