from django.contrib.postgres.fields import ArrayField, HStoreField
from django.db import models

from mdta.apps.users.models import HumanResource


class Project(models.Model):
    """
    Entry of each project which will be represented to Model Driven Graph
    """
    name = models.CharField(max_length=50, unique=True, default='')

    lead = models.ForeignKey(HumanResource, related_name='project_lead', null=True, blank=True)
    members = models.ManyToManyField(HumanResource, related_name='project_members', blank=True)

    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def nodes(self):
        data = []
        for module in self.modules:
            data += module.nodes

        return data

    @property
    def nodes_count(self):
        return len(self.nodes)

    @property
    def edges(self):
        data = []
        for module in self.modules:
            for edge in module.edges:
                if edge not in data:
                    data.append(edge)

        return data

    @property
    def edges_count(self):
        return len(self.edges)

    @property
    def modules_count(self):
        return len(self.module_set.all())

    @property
    def modules(self):
        return self.module_set.order_by('name')

    @property
    def edges_between_modules(self):
        data = []

        for edge in self.edges:
            if edge.from_node.module != edge.to_node.module:
                data.append(edge)

        return data


class Module(models.Model):
    """
    Modules per project
    """
    name = models.CharField(max_length=50, default='')
    project = models.ForeignKey(Project)

    class Meta:
        unique_together = ('project', 'name',)

    def __str__(self):
        return '{0}: {1}'.format(self.project.name, self.name)

    @property
    def nodes(self):
        return self.node_set.order_by('name')

    @property
    def edges(self):
        data = []
        for node in self.nodes:
            data += node.from_node.all()
            data += node.to_node.all()

        return set(data)  # remove duplicate edges


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
