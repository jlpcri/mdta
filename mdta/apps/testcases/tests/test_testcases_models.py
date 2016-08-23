from django.test import TestCase
from django.utils.timezone import localtime

from mdta.apps.projects.models import Project
from mdta.apps.testcases.models import TestCaseResults


class TestCaseHistoryModelTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            name='Test Project'
        )

    def test_string_representation(self):
        test_case_result = TestCaseResults.objects.create(
            project=self.project,
            results=dict()
        )

        self.assertEqual(str(test_case_result), '{0}: {1}'.format(self.project.name,
                                                                  localtime(test_case_result.updated)))

    def test_verbose_name_plural(self):
        self.assertEqual(str(TestCaseResults._meta.verbose_name_plural), 'test case resultss')

