from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.timezone import localtime

from mdta.apps.projects.models import Project


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
