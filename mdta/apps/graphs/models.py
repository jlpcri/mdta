from django.db import models
from django.contrib.postgres.fields import HStoreField, ArrayField

from mdta.apps.projects.models import Project, Module


class NodeType(models.Model):
    """
    Type of Node: Transfer, Prompt, DBRequest, DBResponse,
    HostRequest, HostResponse, Segment
    """
    name = models.CharField(max_length=50, unique=True, default='')

    # Keys of Node property data
    # Start and End Node: empty
    # Transfer: dialed, reason, status, subreason, transfer_type etc
    # Prompt: response_type, response, status, confidence, utterance, grammar, module
    # DatabaseRequest: status, host_key, data_sent
    # DatabaseResponse: host_key, xml_tag_key, xml_tag_value, xml_sequence_number
    # HostRequest: status, host_key, data_sent
    # HostResponse: host_key, xml_tag_key, xml_tag_value, xml_sequence_number
    # Segment: segment_group, segment_name
    keys = ArrayField(models.CharField(max_length=50), null=True, blank=True,
                      verbose_name='Keys(Separated with comma)')

    def __str__(self):
        return '{0}: {1}'.format(self.name, self.keys)


class EdgeType(models.Model):
    """
    Type of Edge: DTMF,
    """
    name = models.CharField(max_length=50, unique=True, default='')

    # Keys of Edge property data
    keys = ArrayField(models.CharField(max_length=50), null=True, blank=True,
                      verbose_name='Keys(Separated with comma)')

    def __str__(self):
        return '{0}: {1}'.format(self.name, self.keys)


# class Module(models.Model):
#     """
#     Modules per project
#     """
#     name = models.CharField(max_length=50, default='')
#     project = models.ForeignKey(Project)


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
    data = HStoreField(null=True, blank=True)

    def __str__(self):
        return '{0}: {1}: {2}'.format(self.project.name, self.name, self.type.name)


class Edge(models.Model):
    """
    Edge between two Nodes to represent the relation of them
    """
    module = models.ForeignKey(Module)
    type = models.ForeignKey(EdgeType)

    name = models.TextField(default='')
    priority = models.SmallIntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(auto_now=True, db_index=True)

    from_node = models.ForeignKey(Node, related_name='from_node')
    to_node = models.ForeignKey(Node, related_name='to_node')

    # Property for the Edge, Keys are from EdgeType
    data = HStoreField(null=True, blank=True)

    def __str__(self):
        return '{0}: {1}: {2}'.format(self.project.name, self.name, self.type.name)


