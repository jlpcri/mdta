from django.test import TestCase

from mdta.apps.projects.models import TestRailInstance, TestRailConfiguration, CatalogItem, Project, Module


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


