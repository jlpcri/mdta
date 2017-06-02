from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.postgres.fields import HStoreField, ArrayField, JSONField

from mdta.apps.projects.models import Project, Module


class NodeType(models.Model):
    """
    Type of Node: DataQueries Database, DataQueries WebService
                  Language
                  Language Audio Path
                  Play Prompt
                  Menu Prompt, Menu Prompt with Confirmation
                  Start
                  TestHeader Start
                  TestHeader End
    """
    name = models.CharField(max_length=50, unique=True, default='')

    keys = ArrayField(models.CharField(max_length=50), null=True, blank=True,
                      verbose_name='Keys(Separated with comma)')
    subkeys = ArrayField(models.CharField(max_length=50), null=True, blank=True,
                         verbose_name='SubKeys(Separated with comma)')

    verbiage_keys = ArrayField(models.CharField(max_length=50), null=True, blank=True,
                               verbose_name='VerbiageKeys(Separated with comma)')

    def __str__(self):
        return '{0}: {1}'.format(self.name, self.keys)

    class Meta:
        ordering = ['name']

    @property
    def keys_data_name(self):
        for item in self.keys:
            if 'Data' in item:
                return item
        return None

    @property
    def subkeys_data_name(self):
        if 'DataQueries' in self.name:
            return self.subkeys
        else:
            if self.subkeys[0]:
                return self.subkeys[0]
            else:
                return None


class EdgeType(models.Model):
    """
    Type of Edge: DTMF,
    """
    name = models.CharField(max_length=50, unique=True, default='')

    # Keys of Edge property data
    keys = ArrayField(models.CharField(max_length=50), null=True, blank=True,
                      verbose_name='Keys(Separated with comma)')
    subkeys = ArrayField(models.CharField(max_length=50), null=True, blank=True,
                         verbose_name='SubKeys(Separated with comma)')

    def __str__(self):
        return '{0}: {1}'.format(self.name, self.keys)

    class Meta:
        ordering = ['name']

    @property
    def keys_data_name(self):
        for item in self.keys:
            if 'Data' in item or 'Condition' in item:
                return item
        return None

    @property
    def subkeys_data_name(self):
        if self.subkeys[0]:
            return self.subkeys[0]
        else:
            return None


class Node(models.Model):
    """
    Node in Model driven Graph represents Transfers, Prompts, DBRequests etc.
    """
    module = models.ForeignKey(Module)
    type = models.ForeignKey(NodeType)

    name = models.TextField()

    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(auto_now=True, db_index=True)

    # Property for the Node, Keys are from NodeType
    properties = JSONField(null=True, blank=True)

    # Verbiage for the PromptNode, Verbiage_Keys are from NodeType
    verbiage = JSONField(null=True, blank=True)

    class Meta:
        unique_together = ('module', 'name',)

    def clean(self):
        # Node name should be unique for node.module.project
        if self.module.project:
            project = self.module.project
            for each_node in project.nodes:
                if each_node.name.casefold() == self.name.casefold() and each_node.id != self.id:
                    if each_node.module == self.module:
                        msg = 'Node with this Module and Name already exists.'
                    else:
                        msg = 'Node with this Project and Name already exists.'
                    raise ValidationError({
                        'name': msg
                    })

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Node, self).save(*args, **kwargs)

    def __str__(self):
        return '{0}: {1}: {2}'.format(self.module, self.name, self.type.name)

    @property
    def edges_count(self):
        if self.from_node:
            return self.from_node.all().count()
        else:
            return 0

    @property
    def leaving_edges(self):
        return self.from_node.select_related('to_node', 'type').order_by('priority')

    @property
    def arriving_edges(self):
        return self.to_node.select_related('from_node', 'type').order_by('priority')

    @property
    def properties_sorted(self):
        return sorted(self.properties.items())

    @property
    def children(self):
        data = []
        for edge in self.leaving_edges:
            data.append(edge.to_node)

        # print(self.name, data)
        return data


class Edge(models.Model):
    """
    Edge between two Nodes (Same Project) to represent the relation of them
    """
    PRIORITY_CHOICES = tuple(((x, x) for x in range(10)))
    type = models.ForeignKey(EdgeType)

    # name = models.TextField(default='')
    priority = models.SmallIntegerField(choices=PRIORITY_CHOICES, default=0)

    celery_visited = models.TextField(default=False)

    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(auto_now=True, db_index=True)

    from_node = models.ForeignKey(Node, related_name='from_node')
    to_node = models.ForeignKey(Node, related_name='to_node')

    # Property for the Edge, Keys are from EdgeType
    properties = JSONField(null=True, blank=True)

    def __str__(self):
        return '{0}: {1}: {2}'.format(self.from_node.module.name, self.from_node.name, self.to_node.name)

    @property
    def properties_sorted(self):
        return sorted(self.properties.items())
