from __future__ import print_function
import mdta.apps.testcases.testrail as testrail


class TestRailORM(object):
    def __init__(self, instance, api_return):
        """Takes JSON from API call and returns a wrapped object"""
        try:
            self.instance = instance
            for k, v in api_return.items():
                self.__dict__[k] = v
        except KeyError as e:
            print("Problem parsing api_return")
            print(api_return)
            raise e

    def client(self):
        client = testrail.APIClient(self.instance.host)
        client.user = self.instance.username
        client.password = self.instance.password
        return client


class TestRailProject(TestRailORM):
    def get_suites(self):
        return [TestRailSuite(self.instance, res) for res in self.client().send_get('get_suites/{0}'.format(self.id))]


class TestRailSuite(TestRailORM):
    def get_cases(self):
        return [TestRailCase(self.instance, res)
                for res in self.client().send_get('get_cases/{0}&suite_id={1}'.format(self.project_id, self.id))]


class TestRailCase(TestRailORM):
    @property
    def custom_steps_separated(self):
        """Because someone made this field with a typo and it can't be changed."""
        return self.custom_steps_seperated


def get_testrail_project(instance, identifier):
    """Returns a TestRail project by name or id"""
    # Name or id?
    if type(identifier) is int:
        project = _get_testrail_project_by_id(instance, identifier)
    elif type(identifier) in [str, unicode]:
        if identifier.isdigit():
            project = _get_testrail_project_by_id(instance, identifier)
        else:
            project = _get_testrail_project_by_name(instance, identifier)
    else:
        raise ValueError("Identifier must be of type int, str, or unicode")
    return project


def _get_testrail_project_by_id(instance, identifier):
    client = testrail.APIClient(instance.host)
    client.user = instance.username
    client.password = instance.password

    return TestRailProject(instance, client.send_get('get_project/{0}'.format(identifier)))


def _get_testrail_project_by_name(instance, identifier):
    raise NotImplementedError
