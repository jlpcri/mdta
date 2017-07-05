import json
import time

from django.test import TestCase

from mdta.celery_module import app
from mdta.apps.runner.models import TestRun, AutomatedTestCase
from mdta.apps.testcases.testrail import APIClient
from mdta.apps.projects.models import TestRailInstance
from mdta.apps.runner.tasks import poll_result_loop


class TestPollResultLoop(TestCase):

    def testNoError(self):
        result = poll_result_loop.delay(8)

        self.assertEquals(result.get(), None)
        self.assertTrue(result.successful())
