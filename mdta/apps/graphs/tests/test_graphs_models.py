from django.test import TestCase
from django.core.urlresolvers import reverse

from mdta.apps.graphs.models import EdgeType, Edge, NodeType, Node
from mdta.apps.projects.models import Project, Module
from mdta.apps.graphs.forms import *

class NodeTypeTest(TestCase):
    def setUp(self):
        self.type_db = NodeType.objects.create(
            name='DataQueries Database',
            keys=['InputData'],
            subkeys=['Inputs, Outputs']
        )
        self.type_prompt = NodeType.objects.create(
            name='Menu Prompt',
            keys=['Verbiage', 'TranslateVerbiage', 'NonStandardFail'],
            subkeys=['OnFailGoTo', 'NM1', 'NI1']
        )
        self.type_transfer = NodeType.objects.create(
            name='dtmp',
            keys=['TransferNumber'],
            subkeys=['']
        )

    def test_keys_data_name_with_data_node(self):
        self.assertEqual(self.type_db.keys_data_name, self.type_db.keys[0])

    def test_keys_data_name_without_data_node(self):
        self.assertEqual(self.type_prompt.keys_data_name, None)

    def test_subkeys_data_name_with_data_node(self):
        self.assertEqual(self.type_db.subkeys_data_name, self.type_db.subkeys)

    def test_subkeys_data_name_without_data_node_with_subkeys(self):
        self.assertEqual(self.type_prompt.subkeys_data_name, 'OnFailGoTo')

    def test_subkeys_data_name_without_data_node_without_subkeys(self):
        self.assertEqual(self.type_transfer.subkeys_data_name, None)


class EdgeTypeTest(TestCase):
    def setUp(self):
        self.type_data = EdgeType.objects.create(
            name='data edge',
            keys=['OutputData', 'Invisible'],
            subkeys=['Outputs']
        )
        self.type_precondition = EdgeType.objects.create(
            name='pre condition',
            keys=['OutputData', 'Invisible'],
            subkeys=['Condition']
        )
        self.type_dtmf = EdgeType.objects.create(
            name='dtmf',
            keys=['Press', 'Invisible'],
            subkeys=['']
        )

    def test_keys_data_name_data(self):
        self.assertEqual(self.type_data.keys_data_name, 'OutputData')

    def test_keys_data_name_precondition(self):
        self.assertEqual(self.type_precondition.keys_data_name, 'OutputData')

    def test_keys_data_name_else(self):
        self.assertEqual(self.type_dtmf.keys_data_name, None)

    def test_subkeys_data_name_with_subkeys(self):
        self.assertEqual(self.type_data.subkeys_data_name, 'Outputs')
        self.assertEqual(self.type_precondition.subkeys_data_name, 'Condition')

    def test_subkeys_data_name_without_subkeys(self):
        self.assertEqual(self.type_dtmf.subkeys_data_name, None)


class NodeTest(TestCase):
    def setUp(self):
        self.test_header = Module.objects.create(
            name='test header'
        )
        self.project = Project.objects.create(
            name='Test Project',
            test_header=self.test_header
        )
        self.module = Module.objects.create(
            name='module1',
            project=self.project
        )
        self.node_type_prompt = NodeType.objects.create(
            name='Menu Prompt',
            keys=['Verbiage', 'TranslateVerbiage', 'NonStandardFail'],
            subkeys=['OnFailGoTo', 'NM1', 'NI1']
        )

    def test_new_node_to_test_header(self):
        th = Node.objects.create(
            name='th start',
            module=self.test_header,
            type=self.node_type_prompt
        )
        self.assertEqual(th.module.name, self.test_header.name)

    def test_new_node_to_module(self):
        node = Node.objects.create(
            name='th start',
            module=self.module,
            type=self.node_type_prompt
        )
        self.assertEqual(node.module.name, self.module.name)
        self.assertEqual(node.module.project.name, self.project.name)

class EdgeNewTest(TestCase):

    def setUp(self):
            self.type_data = EdgeType.objects.create(
                name='data edge',
                keys=['OutputData', 'Invisible'],
                subkeys=['Outputs']
            )
            self.type_precondition = EdgeType.objects.create(
                name='pre condition',
                keys=['OutputData', 'Invisible'],
                subkeys=['Condition']
            )
            self.type_dtmf = EdgeType.objects.create(
                name='dtmf',
                keys=['Press', 'Invisible'],
                subkeys=['']
            )

    def test_new_edge(self):
        response = self.client.post(reverse('edge_type_new'))
        self.assertEqual(response.status_code, 200)

    def test_form_edge(self):
        response = self.client.post('/edge_type_new/', {'name': "" ,'keys':"",'subkeys':"" }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(form.is_valid())

    def test_duplicate_keys(self):
        self.type_data = EdgeType.objects.create()
        Edge.object.create(name='dtmf',keys=['Press', 'Invisible'],subkeys=[''])
        with self.assertRaises(ValidationError):
            edge = Edge(name='dtmf',keys=['Press', 'Invisible'],subkeys=[''])
            edge.full_clean()








