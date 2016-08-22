from django.test import TestCase

from mdta.apps.projects.models import Project, Module


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


