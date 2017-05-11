from django.test import TestCase

from mdta.apps.runner.utils import get_testrail_project
from mdta.apps.projects.models import TestRailInstance


class TestRailInterface(TestCase):
    """
    Attempts to create a test run based on a known suite. Really only appropriate for development checks.
    """
    def test_testrun_context_manager(self):
        tri = TestRailInstance(host='http://linux3216.wic.west.com/testrail',
                               username='testrail@west.com',
                               password='dQadQPZ1NrSwFEZsCNvm-1dGqYePkQ8KjKpn7.mKd')
        trp = get_testrail_project(tri, 6)  # test
        trs = trp.get_suites()[7]  # HAT Generation Testbed
        with trs.test_run() as trr:
            print("Testrun id: {0}".format(trr.id))
        self.assertIsNotNone(trr)

    def test_testrun_generation(self):
        tri = TestRailInstance(host='http://linux3216.wic.west.com/testrail',
                               username='testrail@west.com',
                               password='dQadQPZ1NrSwFEZsCNvm-1dGqYePkQ8KjKpn7.mKd')
        trp = get_testrail_project(tri, 6)  # test
        trs = trp.get_suites()[7]  # HAT Generation Testbed
        trs.test()  # General check for no errors