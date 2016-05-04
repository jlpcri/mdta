from django.db import models
from django.contrib.postgres.fields import HStoreField, ArrayField

from model_driven.apps.projects.models import Project


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
    keys = ArrayField(models.CharField(max_length=50), null=True)

    def __unicode__(self):
        return '{0}: {1}'.format(self.name, self.keys)


class EdgeType(models.Model):
    """
    Type of Edge: DTMF,
    """
    name = models.CharField(max_length=50, unique=True, default='')

    # Keys of Edge property data
    keys = ArrayField(models.CharField(max_length=50), null=True)

    def __unicode__(self):
        return '{0}: {1}'.format(self.name, self.keys)


class Node(models.Model):
    """
    Node in Model driven Graph represents Transfers, Prompts, DBRequests etc.
    """
    project = models.ForeignKey(Project)
    type = models.ForeignKey(NodeType)

    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')
    name = models.TextField()

    # Property for the Node, Keys are from NodeType
    data = HStoreField()

    def __unicode__(self):
        return '{0}: {1}: {2}'.format(self.name, self.project.name, self.type.name)


class Edge(models.Model):
    """
    Edge between two Nodes to represent the relation of them
    """
    project = models.ForeignKey(Project)
    type = models.ForeignKey(EdgeType)

    from_node = models.ForeignKey(Node, related_name='from_node')
    to_node = models.ForeignKey(Node, related_name='to_node')

    # Property for the Node, Keys are from EdgeType
    data = HStoreField()

    def __unicode__(self):
        return '{0}: {1}: {2}'.format(self.name, self.project.name, self.type.name)


