from django.contrib.postgres.fields import ArrayField
from django.db import models

from mdta.apps.users.models import HumanResource


class TestRailInstance(models.Model):
    """
    Configuration of TestRail host
    """
    host = models.URLField()
    username = models.TextField()
    password = models.TextField()

    def __str__(self):
        return '{0}'.format(self.host)


class TestRailConfiguration(models.Model):
    """
    Configuration connect to TestRail
    """
    instance = models.ForeignKey(TestRailInstance, blank=True, null=True)
    project_name = models.TextField()
    test_suite = ArrayField(models.CharField(max_length=200), blank=True)

    def __str__(self):
        return '{0}: {1}'.format(self.project_name, self.test_suite)


class Project(models.Model):
    """
    Entry of each project which will be represented to Model Driven Graph
    """
    name = models.CharField(max_length=50, unique=True, default='')
    testrail = models.ForeignKey(TestRailConfiguration, blank=True, null=True)

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
            for edge in module.edges_all:
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
        """
        Nodes inside Module
        """
        return self.node_set.order_by('name')

    @property
    def edges_all(self):
        """
        Edges inside/leaving/arriving Module
        """
        data = []
        for node in self.nodes:
            data += node.from_node.all()
            data += node.to_node.all()

        return set(data)  # remove duplicate edges

    @property
    def nodes_all(self):
        """
        Nodes inside Module, outside Module which has edge leaving/arriving Module
        """
        data = []
        for edge in self.edges_all:
            if edge.from_node not in data:
                data.append(edge.from_node)
            if edge.to_node not in data:
                data.append(edge.to_node)

        for node in self.nodes:
            if node not in data:
                data.append(node)

        return data


class CatalogItem(models.Model):
    """
    West service catalog item,
    Five hierarchy: component, offering, feature, functionality, product
    """
    project = models.ManyToManyField(Project)
    name = models.TextField()
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children_set')
    description = models.TextField(blank=True)

    def __str__(self):
        if self.parent:
            return '{0}: {1}'.format(self.parent.name, self.name)
        else:
            return '{0}'.format(self.name)

    class Meta:
        unique_together = ('parent', 'name')
