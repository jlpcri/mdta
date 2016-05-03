from django.db import models

from model_driven.apps.users.models import HumanResource


class Project(models.Model):
    """
    Entry of each project which will be represented to Model Driven Graph
    """
    name = models.CharField(max_length=50, unique=True, default='')

    lead = models.ForeignKey(HumanResource, related_name='lead', blank=True)
    worker = models.ManyToManyField(HumanResource, related_name='worker', blank=True)

    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(auto_now=True, db_index=True)

    def __unicode__(self):
        return self.name

