from django.contrib.postgres.fields import ArrayField, HStoreField
from django.db import models

from mdta.apps.projects.models import Project


class TestCaseHistory(models.Model):
    """
    Latest 3 Test cases set per project
    """
    name = models.CharField(max_length=50, default='')
    project = models.ForeignKey(Project)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(auto_now=True, db_index=True)
    results = ArrayField(HStoreField(), blank=True, null=True)

    def __str__(self):
        return '{0}: {1}: {2}'.format(self.project.name,
                                      self.name,
                                      self.created)
