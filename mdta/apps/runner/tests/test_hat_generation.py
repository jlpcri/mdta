from django.test import TestCase

from mdta.apps.runner.utils import HATScript

class BasicConnectionToLab(TestCase):
    """
    Ill-advised test that ensures we can connect to the QA lab and run a basic HAT script
    on the current machine.
    """
    def test_startcall_recognition(self):
        hs = HATScript()
        hs.basic_connection_test()
        response = hs.hatit_execute()
        self.assertEqual(200, response.status_code, 'test_startcall_recognition received a status code other than 200')
