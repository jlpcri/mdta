from django.contrib.postgres.fields import JSONField, ArrayField
from django.db import models
from django.utils.timezone import localtime

from mdta.apps.projects.models import Project


class TestRailInstance(models.Model):
    """
    Configuration of TestRail host
    """
    host = models.URLField()
    username = models.TextField()
    password = models.TextField()

    def __str__(self):
        return '{0}: {1}'.format(self.host, self.username)


class TestRailConfiguration(models.Model):
    """
    Configuration connect to TestRail
    project_name: Name of project in TestRail
    project_id: Id of project in TestRail
    """
    instance = models.ForeignKey(TestRailInstance, blank=True, null=True)
    project_name = models.TextField(unique=True)
    project_id = models.CharField(max_length=20, blank=True, null=True)
    test_suite = ArrayField(models.CharField(max_length=200), blank=True, null=True)

    def __str__(self):
        return '{0}: {1}'.format(self.project_name, self.project_id)

    class Meta:
        ordering = ['project_name']


class TestCaseResults(models.Model):
    """
    Latest 3 Test cases set per project
    """
    # name = models.CharField(max_length=50, default='')
    project = models.ForeignKey(Project)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(auto_now=True, db_index=True)
    results = JSONField()

    def __str__(self):
        return '{0}: {1}'.format(self.project.name,
                                 localtime(self.updated))
