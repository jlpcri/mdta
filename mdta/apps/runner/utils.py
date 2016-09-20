class TestRailProject(object):
    def __init__(self, api_return):
        """Takes JSON from API call and returns a wrapped object"""
        self.name = api_return['name']
        self.id = api_return['id']
        self.url = api_return['url']
        self.is_completed = api_return['is_completed']
        self.completed_on = api_return['completed_on']


def get_testrail_project(identifier):
    """Returns a TestRail project by name or id"""
    # Name or id?
    if type(identifier) is int:
        project = _get_testrail_project_by_id(identifier)
    elif type(identifier) in [str, unicode]:
        if identifier.isdigit():
            project = _get_testrail_project_by_id(identifier)
        else:
            project = _get_testrail_project_by_name(identifier)
    else:
        raise ValueError("Identifier must be of type int, str, or unicode")
    return project


def _get_testrail_project_by_id(identifier):
    raise NotImplementedError


def _get_testrail_project_by_name(identifier):
    raise NotImplementedError
