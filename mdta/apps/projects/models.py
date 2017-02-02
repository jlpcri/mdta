from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
import time

from mdta.apps.users.models import HumanResource
import mdta.apps.graphs.models


class TestRailInstance(models.Model):
    """
    Configuration of TestRail host
    """
    host = models.URLField()
    username = models.TextField()
    password = models.TextField()

    def __str__(self):
        return '{0}: {1}'.format(self.host, self.username)

    @property
    def host_abbreviation(self):
        abbr = self.host.split('.')
        abbr_last = abbr[len(abbr) - 1].split('/')

        return abbr[0] + '/' + abbr_last[-1]


class TestRailConfiguration(models.Model):
    """
    Configuration connect to TestRail
    project_name: Name of project in TestRail
    project_id: Id of project in TestRail
    """
    instance = models.ForeignKey(TestRailInstance, blank=True, null=True)
    project_name = models.TextField(unique=True)
    project_id = models.CharField(max_length=20, blank=True, null=True)
    test_suite = ArrayField(models.CharField(max_length=200), blank=True, null=True)

    def __str__(self):
        return '{0}: {1}'.format(self.project_name, self.project_id)

    class Meta:
        ordering = ['project_name']


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
    test_header = models.ForeignKey('Module', null=True, blank=True,
                                    related_name='test_header')

    version = models.TextField()  # relate to TestRail-TestSuites
    testrail = models.ForeignKey(TestRailConfiguration,
                                 models.SET_NULL,
                                 blank=True,
                                 null=True,)
    catalog = models.ManyToManyField(CatalogItem, blank=True)
    # vuid = models.ForeignKey('Module', null=True, on_delete=models.SET_NULL)

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
        return Node.objects.select_related('module').filter(module__project=self).order_by('module', 'name')

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
        Edge = mdta.apps.graphs.models.Edge  # avoiding circular import
        data = []

        for module in self.modules:
            cross_module_edges = Edge.objects.filter(from_node__module=module).exclude(to_node__module=module)
            data.extend(cross_module_edges)

        return data


class Module(models.Model):
    """
    Modules per project
    """
    name = models.CharField(max_length=50, default='')
    project = models.ForeignKey(Project, null=True, blank=True)  # if null, then it's Test Header
    catalog = models.ManyToManyField(CatalogItem, blank=True)

    class Meta:
        ordering = ['name']
        unique_together = ('project', 'name',)

    def __str__(self):
        if self.project:
            return '{0}: {1}'.format(self.project.name, self.name)
        else:
            return '{0}: {1}'.format('TestHeader', self.name)

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
        return Edge.objects.select_related('from_node', 'to_node', 'type').filter(Q(from_node__in=nodes) | Q(to_node__in=nodes)).distinct()

    @property
    def nodes_all(self):
        """
        Nodes inside Module, outside Module which has edge leaving/arriving Module
        """
        Node = mdta.apps.graphs.models.Node  # avoiding circular import
        edges = self.edges_all
        return Node.objects.select_related('type', 'module').filter(Q(from_node__in=edges) | Q(to_node__in=edges) | Q(module=self)).distinct()

    @property
    def th_related_projects(self):
        """
        Projects which test_header refers to this Module instance
        :return:
        """
        data = []
        projects = Project.objects.filter(test_header=self)
        for project in projects:
            data.append({
                'name': project.name,
                'id': project.id
            })

        return data

    @property
    def data_autocomplete(self):
        """
        Get node DataQueries Database/ DataQueries WebService, node.properties['InputData']['Outputs'] keys
        As data edge Follow if  keys
        """
        Node = mdta.apps.graphs.models.Node  # avoiding circular import

        node_names = []
        data_edge_keys = []
        menu_prompt_outputs_keys = []

        try:
            if self.project:
                node_names = Node.objects.filter(module__project=self.project).values_list('name', flat=True).order_by('name')
                for module in self.project.modules:
                    for node in module.nodes.filter(type__name__in=['DataQueries Database', 'DataQueries WebService']):
                        for item in node.properties[node.type.keys_data_name]:
                            for key in item['Outputs'].keys():
                                tmp = {
                                    'label': key + ': ' + item['Outputs'][key],
                                    'value': '{{\'{0}\': \'{1}\'}}'.format(key, item['Outputs'][key])
                                }
                                if tmp not in data_edge_keys:
                                    data_edge_keys.append(tmp)
                            for key in item['Inputs'].keys():
                                if key not in menu_prompt_outputs_keys:
                                    menu_prompt_outputs_keys.append(key)

                data_edge_keys = sorted(data_edge_keys, key=lambda k: k['label'])
            else:
                node_names = Node.objects.filter(module=self).values_list('name', flat=True).order_by('name')

        except TypeError:
            pass

        data = {
            'node_names': node_names,
            'data_edge_keys': data_edge_keys,
            'menu_prompt_outputs_keys': menu_prompt_outputs_keys
        }

        # print(node_names)
        return data


class ProjectVariable(models.Model):
    """
    Variables of project level
    """
    TESTHEADER = 1
    PRECONDITION = 2
    PROMPT = 3
    DATA = 4
    ORIGIN_TYPE_CHOICES = (
        (TESTHEADER, 'TestHeader'),
        (PRECONDITION, 'PreCondition'),
        (PROMPT, 'Prompt'),
        (DATA, 'Data')
    )

    project = models.ForeignKey(Project)
    name = models.TextField()
    origin_type = models.IntegerField(choices=ORIGIN_TYPE_CHOICES, default=TESTHEADER)
    origin = models.ForeignKey('graphs.Node', null=True, blank=True)

    class Meta:
        ordering = ['name']
        unique_together = ('project', 'name',)

    def __str__(self):
        return '{0}: {1}'.format(self.project.name, self.name)


def vuid_location(instance, filename):
    return "{0}_{1}".format(str(time.time()).replace('.', ''), filename)


class VUID(models.Model):
    """Represents the uploaded file used to generate VoiceSlot object"""
    project = models.ForeignKey(Project)
    filename = models.TextField()
    upload_date = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to=vuid_location)
    upload_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return '{0}: {1}'.format(self.filename, self.project.name)
