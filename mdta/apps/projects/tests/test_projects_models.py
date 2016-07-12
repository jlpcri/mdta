from django.test import TestCase

from mdta.apps.projects.models import Project, Module, TestCaseHistory


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


class TestCaseHistoryModelTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            name='Test Project'
        )

    def test_string_representation(self):
        test_case_history = TestCaseHistory.objects.create(
            name='Test Case History',
            project=self.project
        )

        self.assertEqual(str(test_case_history), '{0}: {1}: {2}'.format(self.project.name,
                                                                        test_case_history.name,
                                                                        test_case_history.created))

    def test_verbose_name_plural(self):
        self.assertEqual(str(TestCaseHistory._meta.verbose_name_plural), 'test case historys')

