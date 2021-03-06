from django.test import TestCase

from mdta.apps.runner.utils import HATScript


class BasicConnectionToLab(TestCase):
    """
    Ill-advised test that ensures we can connect to the QA lab and run a basic HAT script.
    """
    def test_startcall_recognition(self):
        hs = HATScript()
        hs.remote_server = 'qaci01.wic.west.com'
        hs.remote_user = 'wicqacip'
        hs.remote_password = 'LogFiles'
        hs.basic_connection_test()
        response = hs.remote_hat_execute()
        print(hs.results())


class TestHatScript(object):
    def __init__(self, wrapped_class, *args, **kargs):
        self.wrapped_class = wrapped_class(*args, **kargs)

    def basic_connection_test(self):
        pass

    def hatit_execute(self):
        pass




