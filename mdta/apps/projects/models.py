from django.db import models
from django.db.models import Q

from mdta.apps.users.models import HumanResource
import mdta.apps.graphs.models


class CatalogItem(models.Model):
    """
    West service catalog item,
    Five hierarchy: component, offering, feature, functionality, product
    """
    # project = models.ManyToManyField(Project, blank=True)
    name = models.TextField()
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children_set')
    description = models.TextField(blank=True)

    def __str__(self):
        if self.parent:
            return '{0}: {1}'.format(self.name, self.parent.id)
        else:
            return '{0}'.format(self.name)

    class Meta:
        unique_together = ('parent', 'name')


class Project(models.Model):
    """
    Entry of each project which will be represented to Model Driven Graph
    """
    name = models.CharField(max_length=50, unique=True, default='')

    version = models.TextField()  # relate to TestRail-TestSuites
    testrail = models.ForeignKey('testcases.TestRailConfiguration',
                                 models.SET_NULL,
                                 blank=True,
                                 null=True,)
    catalog = models.ManyToManyField(CatalogItem, blank=True)

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
        Node = mdta.apps.graphs.models.Node  # avoiding circular import
        return Node.objects.filter(module__project=self)

    @property
    def nodes_count(self):
        return self.nodes.count()

    @property
    def edges(self):
        Edge = mdta.apps.graphs.models.Edge  # avoiding circular import
        return Edge.objects.filter(from_node__module__project=self)

    @property
    def edges_count(self):
        return self.edges.count()

    @property
    def modules_count(self):
        return self.module_set.all().count()

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
    catalog = models.ManyToManyField(CatalogItem, blank=True)

    class Meta:
        ordering = ['name']
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
        Edge = mdta.apps.graphs.models.Edge  # avoiding circular import
        nodes = self.node_set.all()
        return Edge.objects.filter(Q(from_node__in=nodes) | Q(to_node__in=nodes)).distinct()

    @property
    def nodes_all(self):
        """
        Nodes inside Module, outside Module which has edge leaving/arriving Module
        """
        Node = mdta.apps.graphs.models.Node  # avoiding circular import
        edges = self.edges_all
        return Node.objects.filter(Q(from_node__in=edges) | Q(to_node__in=edges) | Q(module=self)).distinct()



