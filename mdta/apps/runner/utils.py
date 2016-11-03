from __future__ import print_function
import textwrap
from tempfile import NamedTemporaryFile
import os
import sys
import time

import requests
from paramiko.client import AutoAddPolicy
from paramiko import SSHClient, SFTPClient, Transport

import mdta.apps.testcases.testrail as testrail

if os.name == 'posix' and sys.version_info[0] < 3:
    import subprocess32 as subprocess
else:
    import subprocess


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
    def __init__(self, instance, api_return):
        super(TestRailCase, self).__init__(instance, api_return)
        self.script = None

    @property
    def custom_steps_separated(self):
        """Because someone made this field with a typo and it can't be changed."""
        if "custom_steps_separated" not in self.__dict__.keys():
            return self.custom_steps_seperated
        else:
            return self.__dict__['custom_steps_separated']

    def generate_hat_script(self):
        if not self.script:
            self.script = HATScript()
        for step in self.custom_steps_separated:
            print("STEP: {0}".format(step))
            self._content_routing(step['content'])
            self._expected_routing(step['expected'])
            print("BODY: {0}".format(self.script.body))
        print ("END OF STEPS")
        self.script.end_of_call()
        print("BODY: {0}".format(self.script.body))

    def _content_routing(self, step):
        if not step:
            return
        action = step.split(' ')[0].upper()
        action = action.replace(":", "")
        action_map = {'DNIS': self.script.start_of_call,
                      'DIAL': self.script.start_of_call,
                      'DIALEDNUMBER:': self.script.start_of_call,
                      'APN': self.script.start_of_call,
                      'PRESS': self.script.dtmf_step}
        action_map[action](step)

    def _expected_routing(self, step):
        if not step:
            return
        # The following should be moved to HATScript, but because there is no real branching at this point yet,
        # I'm leaving it as-is for now.
        prompt = step.split(':')[0]
        self.script.body += 'EXPECT prompt URI=audio/' + prompt + '.wav\n'


def get_testrail_steps(instance, case_id):
    client = testrail.APIClient(instance.host)
    client.user = instance.username
    client.password = instance.password

    return TestRailCase(instance, client.send_get('get_case/{0}'.format(case_id)))


def get_testrail_project(instance, identifier):
    """Returns a TestRail project by name or id"""
    # Name or id?
    if type(identifier) is int:
        project = _get_testrail_project_by_id(instance, identifier)
    elif type(identifier) is str:  # Python 3 string are always Unicode
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


class AutomationScript(object):
    NOT_RUN = 0
    PASS = 1
    FAIL = 2

    def results(self):
        return NotImplementedError

    def generate(self):
        return NotImplementedError


class HATScript(AutomationScript):
    def __init__(self, apn='', body='', dialed_number='',
                 holly_server='linux5578.wic.west.com', sonus_server='10.27.138.136',
                 remote_server='qaci01.wic.west.com', remote_user='', remote_password=''):
        self.apn = apn
        self.dialed_number = dialed_number
        self.body = body
        self.filename = ''
        self.holly_server = holly_server
        self.sonus_server = sonus_server
        self.remote_server = remote_server
        self.remote_user = remote_user
        self.remote_password = remote_password

    def basic_connection_test(self):
        """Performs a basic test that should never fail if the HAT server is able to place a call."""
        if not self.apn:
            self.apn = 4061702
        if not self.holly_server:
            self.holly_server = 'linux5578'
        self.body = textwrap.dedent("""\
            STARTCALL
            REPORT MDTA basic connection test
            IGNORE answer asr_session document_dump document_transition fetch grammar_activation license log note prompt recognition_start recognition_end redux severe sip_session system_response transfer_start transfer_end vxml_event vxml_trace warning
            EXPECT call_start
            ENDCALL
            """)

    def hatit_execute(self):
        """Uses Frank's HAT User Interface to initate a HAT test"""
        browser = requests.session()
        browser.get('http://{0}/hatit'.format(self.remote_server))
        csrf_token = browser.cookies['csrftoken']
        data = {'csrfmiddlewaretoken': csrf_token,
                'apn': self.apn,
                'port': '5060',
                'hatscript': self.body}
        response = browser.post("http://{0}/hatit/results/".format(self.hatit_server), data=data)
        browser.close()
        return response

    def local_hat_execute(self):
        """
        Use a HAT instance on the local machine for test execution

        Use in its current state is not recommended. Leaving it in code as a reference.
        """
        try:
            script_file = NamedTemporaryFile(mode='w')
            self.filename = script_file.name
            try:
                subprocess.call(['hat',
                                 '-s', self.filename,
                                 '-p', 'sip:{0}@{1}:5060'.format(self.apn, self.holly_server)])
            except subprocess.CalledProcessError:
                pass  # HAT exiting with a non-zero status code means remarkably little
        finally:
            script_file.close()

    def remote_hat_execute(self):
        """
        Use a HAT instance on a remote machine via SSH
        """
        remote_filename = self._send_hat_script()
        self.filename = remote_filename.split('/')[-1]
        stdin, stdout, stderr = self._invoke_remote_hat()
        time.sleep(2)
        return self._read_remote_results()

    def _send_hat_script(self, dest_directory='/tmp'):
        transport = Transport(self.remote_server, 22)
        transport.connect(username=self.remote_user, password=self.remote_password)
        file_client = SFTPClient.from_transport(transport)

        script_file = NamedTemporaryFile(mode='w', delete=False)
        script_file.write(self.body)
        script_file.close()

        file_client.put(script_file.name, script_file.name)
        file_client.close()
        return script_file.name

    def _invoke_remote_hat(self):
        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.load_system_host_keys()
        client.connect(self.remote_server, username=self.remote_user, password=self.remote_password)
        command = 'hat -s /tmp/{0} -p {1} -i /var/mdta/report/ -o /var/mdta/log/{0}.log -b {2}:4080'.format(
            self.filename, self.sip_string(), self.holly_server)
        print(command)
        f = open('/home/caheyden/last-hat-command', 'w')
        f.write(command)
        f.close()
        conn = client.exec_command(command)
        client.close()
        return conn

    def _read_remote_results(self):
        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.load_system_host_keys()
        client.connect(self.remote_server, username=self.remote_user, password=self.remote_password)
        command = "grep {0} /var/mdta/report/CallReport.log".format(self.filename)
        for i in range(20):
            print("Attempt {0}".format(i))
            stdin, stdout, stderr = client.exec_command(command)
            result_line = stdout.read()
            print(result_line)
            if result_line:
                break
            time.sleep(0.25)
        client.close()
        result_fields = result_line.split(",")
        result = {'result': result_fields[-4], 
                  'reason': result_fields[-2],
                  'call_id': result_fields[2]}
        return result

    def start_of_call(self, step):
        print("start_of_call: {0}".format(step))
        if step[:3].upper() == 'APN':
            self.apn = step[4:].strip()
        elif step[:4].upper() == 'DNIS':
            self.apn = step[5:].strip()
        elif step[:4].upper() == 'DIAL':
            self.dialed_number = step[5:].strip()
        elif step[:4].upper() == 'DIALEDNUMBER:':
            self.dialed_number = step[14:].strip()
        assert (len(self.body) == 0)
        self.body = 'STARTCALL\n' + \
                    'IGNORE answer asr_session document_dump document_transition fetch grammar_activation license ' + \
                    'log note prompt recognition_start recognition_end redux severe sip_session system_response ' + \
                    'transfer_start transfer_end vxml_event vxml_trace warning\n' + \
                    'EXPECT call_start\n'

    def dtmf_step(self, step):
        self.body += 'EXPECT recognition_start\nPAUSE 1\nDTMF ' + step[6:] + '\n'

    def end_of_call(self):
        self.body += 'ENDCALL\n'

    def sip_string(self):
        if self.dialed_number:
            return 'sip:999000017{0}@{1}:5060'.format(self.dialed_number, self.sonus_server)
        else:
            return 'sip:{0}@{1}:5060'.format(self.apn, self.holly_server)


def emergency_test():
    from mdta.apps.projects.models import TestRailInstance
    tri = TestRailInstance.objects.first()
    trp = get_testrail_project(tri, 6)
    c = trp.get_suites()[7].get_cases()[0]
    c.generate_hat_script()
    c.script.remote_user = 'caheyden'
    c.script.remote_password = 'dsi787cAH16'
    conn = c.script.remote_hat_execute()
    return c.id, c.script.filename, conn
