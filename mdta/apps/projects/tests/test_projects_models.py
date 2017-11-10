from django.test import TestCase, Client, RequestFactory
from mdta.apps.projects.models import TestRailInstance, TestRailConfiguration, CatalogItem, Project, Module, User
from mdta.apps.testcases.views import create_testcases

from django.core.urlresolvers import resolve, reverse
from mdta.apps.users.models import HumanResource



class TestRailInstanceTest(TestCase):
    def test_string_representation(self):
        tr_instance = TestRailInstance.objects.create(
            host='http://www.example.com',
            username='Username',
            password='Password'
        )
        self.assertEqual(str(tr_instance), '{0}: {1}'.format(tr_instance.host, tr_instance.username))

    def test_verbose_name_plural(self):
        self.assertEqual(str(TestRailInstance._meta.verbose_name_plural), 'test rail instances')


class TestRailConfigurationTest(TestCase):
    def setUp(self):
        self.tr_instance = TestRailInstance.objects.create(
            host='http://www.example.com',
            username='Username',
            password='Password'
        )

    def test_string_representation(self):
        tr_config = TestRailConfiguration.objects.create(
            instance=self.tr_instance,
            project_name='Project Name',
            project_id=234
        )
        self.assertEqual(str(tr_config), '{0}: {1}'.format(tr_config.project_name,
                                                           tr_config.project_id))

    def test_verbose_name(self):
        self.assertEqual(str(TestRailConfiguration._meta.verbose_name_plural), 'test rail configurations')


class CatalogItemTest(TestCase):
    def setUp(self):
        self.parent_catalog = CatalogItem.objects.create(
            name='Parent Catalog'
        )
        self.child_catalog = CatalogItem.objects.create(
            name='Child Catalog',
            parent=self.parent_catalog
        )

    def test_string_representation(self):
        self.assertEqual(str(self.parent_catalog), self.parent_catalog.name)
        self.assertEqual(str(self.child_catalog), '{0}: {1}'.format(self.child_catalog.name,
                                                                    self.parent_catalog.id))

    def test_verbose_name(self):
        self.assertEqual(str(CatalogItem._meta.verbose_name_plural), 'catalog items')


class ProjectModelTest(TestCase):
    def test_string_representation(self):
        project = Project.objects.create(
            name='Test Project'
        )

        self.assertEqual(str(project), project.name)

    def test_verbose_name_plural(self):
        self.assertEqual(str(Project._meta.verbose_name_plural), 'projects')


class ModuleModelTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            name='Test Project'
        )

    def test_string_representation(self):
        module = Module.objects.create(
            name='Test Module',
            project=self.project
        )

        self.assertEqual(str(module), '{0}: {1}'.format(self.project.name,
                                                        module.name))

    def test_verbose_name_plural(self):
        self.assertEqual(str(Module._meta.verbose_name_plural), 'modules')


class ProjectDatabaseTest(TestCase):
    fixtures = ['test_project']
    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(username='admin')
        self.user_account = {
            'username': 'admin',
            'password': 'redacted'
        }
        self.hr = HumanResource.objects.get(user=User.objects.get(username='admin'))
        self.client.login(
            username=self.user_account['username'],
            password=self.user_account['password']
        )

        self.project = Project.objects.get(name='Test Project')
        self.module = Module.objects.get(name='Test Module')


    def test_create_testcases(self):
        url = reverse('testcases:create_testcases',args=[self.module.id]) + "?level=module"
        response = self.client.get(url)
        self.assertContains(response, "1. Route from &#39;Start&#39; to &#39;testnode&#39;: <br>")
