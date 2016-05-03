from django.db import models

from model_driven.apps.projects.models import Project


class Node(models.Model):
    """
    Node in Model driven Graph represents Transfers, Prompts, DBRequests etc.
    """
    TRANSFER = 1
    PROMPT = 2
    DATABASEREQUEST = 3
    DATABASERESPONSE = 4
    HOSTREQUEST = 5
    HOSTRESPONSE = 6
    SEGMENT = 7
    TYPE_CHOICES = (
        (TRANSFER, 'Transfer'),
        (PROMPT, 'Prompt'),
        (DATABASEREQUEST, 'Database Request'),
        (DATABASERESPONSE, 'Database Response'),
        (HOSTREQUEST, 'Host Request'),
        (HOSTRESPONSE, 'Host Response'),
        (SEGMENT, 'Segment')
    )

    project = models.ForeignKey(Project)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')
    name = models.TextField()
    type = models.IntegerField(choices=TYPE_CHOICES, default=PROMPT)


class Edge(models.Model):
    """
    Edge between two Nodes to represent the relation of them
    """
    project = models.ForeignKey(Project)
    from_node = models.ForeignKey(Node, related_name='from_node')
    to_node = models.ForeignKey(Node, related_name='to_node')


class Transfer(models.Model):
    """
    Transfer type of Node
    """
    node = models.ForeignKey(Node)

    dialed = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    reason = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    subreason = models.TextField(blank=True, null=True)
    transfer_type = models.TextField(blank=True, null=True)


class Prompt(models.Model):
    """
    Prompt type of Node
    """
    node = models.ForeignKey(Node)

    name = models.TextField(blank=True, null=True)
    response_type = models.TextField(blank=True, null=True)
    response = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    confidence = models.IntegerField(blank=True, null=True)
    utterance = models.TextField(blank=True, null=True)
    grammar = models.TextField(blank=True, null=True)
    module = models.TextField(blank=True, null=True)


class DatabaseRequest(models.Model):
    """
    Database Request type of Node
    """
    node = models.ForeignKey(Node)

    name = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    host_key = models.TextField(blank=True, null=True)
    data_sent = models.TextField(blank=True, null=True)


class DatabaseResponse(models.Model):
    """
    Database Response type of Node
    """
    node = models.ForeignKey(Node)

    host_key = models.TextField(blank=True, null=True)
    xml_tag_key = models.TextField(blank=True, null=True)
    xml_tag_value = models.TextField(blank=True, null=True)
    xml_sequence_number = models.IntegerField(null=True)


class HostRequest(models.Model):
    """
    Host Request type of Node
    """
    node = models.ForeignKey(Node)

    name = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    host_key = models.TextField(blank=True, null=True)
    data_sent = models.TextField(blank=True, null=True)


class HostResponse(models.Model):
    """
    Host Response type of Node
    """
    node = models.ForeignKey(Node)

    host_key = models.TextField(blank=True, null=True)
    xml_tag_key = models.TextField(blank=True, null=True)
    xml_tag_value = models.TextField(blank=True, null=True)
    xml_sequence_number = models.IntegerField(null=True)


class Segment(models.Model):
    """
    Segment type of Node
    """
    node = models.ForeignKey(Node)

    segment_group = models.TextField(blank=True, null=True)
    segment_name = models.TextField(blank=True, null=True)
