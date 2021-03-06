from __future__ import print_function
import csv
import textwrap
from contextlib import contextmanager
from tempfile import NamedTemporaryFile
import io
import os
import sys
import time

import datetime
import requests
from paramiko.client import AutoAddPolicy
from paramiko import SSHClient, SFTPClient, Transport

import mdta.settings.base as base

import mdta.apps.testcases.testrail as testrail


if os.name == 'posix' and sys.version_info[0] < 3:
    import subprocess32 as subprocess
else:
    import subprocess


class TestRailORM(object):
    def __init__(self, instance, api_return, parent=None):
        """Takes JSON from API call and returns a wrapped object"""
        self.api_return = api_return
        self.instance = instance
        self.parent = parent
        try:
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
        return [TestRailSuite(self.instance, res, self) for res in self.client().send_get('get_suites/{0}'.format(self.id))]


class TestRailRun(TestRailORM):
    def get_tests(self):
        return [TestRailCase(self.instance, res, self) for res in self.client().send_get('get_tests/{0}'.format(self.id))]


class TestRailSuite(TestRailORM):
    def get_cases(self):
        return [TestRailCase(self.instance, res, self)
                for res in self.client().send_get('get_cases/{0}&suite_id={1}'.format(self.project_id, self.id))]

    def __str__(self):
        return "{0}: {1}".format(self.id, self.name)

    def __repr__(self):
        return str(self)


    @contextmanager
    def test_run(self):
        trr = self.open_test_run()
        yield trr
        self.close_test_run(trr.id)
        return

    def open_test_run(self):
        payload = {'suite_id': self.id}
        res = self.client().send_post('add_run/{0}'.format(self.parent.id), payload)
        trr = TestRailRun(self.instance,
                          self.client().send_post('add_run/{0}'.format(self.parent.id), payload),
                          parent=self)
        return trr

    def close_test_run(self, run_id):
        self.client().send_post('close_run/{0}'.format(run_id), {})

    def test(self):
        with self.test_run() as tr:
            for case in tr.get_tests():
                case.generate_hat_script()
                print(case.script.body)


class TestRailCase(TestRailORM):
    def __init__(self, instance, api_return, parent=None):
        super(TestRailCase, self).__init__(instance, api_return, parent)
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

            self._content_routing(step['content'])
            self._expected_routing(step['expected'])
        self.script.end_of_call()

    def _content_routing(self, step):
        if not step:
            return
        action = step.split(' ')[0].upper()
        action = action.replace(":", "")
        action_map = {'DNIS': self.script.start_of_call,
                      'DIAL': self.script.start_of_call,
                      'DIALEDNUMBER': self.script.start_of_call,
                      'APN': self.script.start_of_call,
                      'HOLLYBROWSER': self.script.start_of_call,
                      'PRESS': self.script.dtmf_step,
                      'WAIT': self.script.no_input,
                       }
        action_map[action](step)
        # try:
        #     action_map[action](step)
        # except KeyError:
        #     pass

    def _expected_routing(self, step):
        if not step:
            return
        # The following should be moved to HATScript, but because there is no real branching at this point yet,
        # I'm leaving it as-is for now.
        # 7/21/2017: read the above comment, put in a branch, still didn't move the code.
        prompt = step.split(':')[0].strip()
        if prompt == '[TTS]':
            self.script.body += 'EXPECT prompt\n'
        else:
            self.script.body += 'EXPECT prompt URI=.*/' + prompt + '.wav\n'


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
    elif type(identifier) in [type(''), type(u'')]:
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

    def __init__(self, apn='', body='', dialed_number='', csvfile='',
                 holly_server='', sonus_server='10.27.138.136',
                 hatit_server='',
                 remote_server='qaci01.wic.west.com', remote_user='wicqacip', remote_password='LogFiles'):

        self.csvfile = csvfile
        self.hatscript = ''
        self.hatit_server = hatit_server
        self.runID = ''
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
        jsonList = []
        browser = requests.session()
        qaci = browser.get('http://{0}/hatit'.format(self.remote_server))
        print(self.hatit_server)
        data = {'apn': self.apn,
                'browser': self.holly_server,
                'port': '5060'}
        hat_script_template = "STARTCALL\nREPORT %id%\n%everything%\nENDCALL"
        path = base.TMP_DIR
        response = browser.post("{0}".format(self.hatit_server) + "api/csv_req/", data=data,
                                 files={'csvfile': open(os.path.join(path, self.csvfile)), 'hatscript': io.StringIO(hat_script_template)})
        jsonList.append(response.json())
        for data in jsonList:
            self.runID = data['runid']
        result = browser.get("{0}".format(self.hatit_server) + "api/check_run/?runid={0}".format(self.runID))
        browser.close()
        return result

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
        self._invoke_remote_hat()
        return self._read_remote_results()

    def _send_hat_script(self, dest_directory='/tmp'):
        transport = Transport(self.remote_server, 22)
        transport.connect(username=self.remote_user, password=self.remote_password)
        file_client = SFTPClient.from_transport(transport)

        script_file = NamedTemporaryFile(mode='w', delete=False)
        script_file.write(self.body)
        script_file.close()
        moveable_script_name = script_file.name + '_'

        file_client.put(script_file.name, moveable_script_name)
        file_client.close()
        return moveable_script_name

    def _invoke_remote_hat(self):
        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.load_system_host_keys()
        client.connect(self.remote_server, username=self.remote_user, password=self.remote_password)
        command = 'hat -s /tmp/{0} -p {1} -i /var/mdta/report/ -o /var/mdta/log/{0}.log -b {2}:4080'.format(
            self.filename, self.sip_string(), self.holly_server)
        print(command)
        channel = client.get_transport().open_session()
        channel.exec_command(command)
        channel.recv_exit_status()
        channel.close()
        client.close()

    def _read_remote_results(self, retry_attempts=3):
        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.load_system_host_keys()
        client.connect(self.remote_server, username=self.remote_user, password=self.remote_password)
        command = "grep {0} /var/mdta/report/CallReport.log".format(self.filename)
        for i in range(15):
            print("Attempt {0}".format(i))
            stdin, stdout, stderr = client.exec_command(command)
            result_line = stdout.read()
            print(result_line)
            if result_line:
                break
            time.sleep(0.25)
        client.close()
        try:
            result_fields = result_line.decode('utf-8').split(",")
            result = {'result': result_fields[-4],
                      'reason': result_fields[-2],
                      'call_id': result_fields[2]}
        except IndexError:
            address_in_use = self._check_call_start_failure()
            if address_in_use:
                if retry_attempts >= 1:
                    time.sleep(6)
                    print("Retries left: {0}".format(retry_attempts-1))
                    self._invoke_remote_hat()
                    result = self._read_remote_results(retry_attempts=retry_attempts-1)
                else:
                    result = {'result': 'FAIL',
                              'reason': 'Unable to place call, port in use',
                              'call_id': '0'}
            elif not result_line:
                result = {'result': 'FAIL',
                          'reason': 'No results for this test case were found in the logs.',
                          'call_id': '0'}
            else:
                result = {'result': 'FAIL',
                          'reason': 'Failed to read results: ' + str(result_line),
                          'call_id': '0'}
        except Exception as e:
            result = {'result': 'FAIL',
                      'reason': 'An untrapped error occurred: ' + str(e.args),
                      'call_id': '0'}
        return result

    def _check_call_start_failure(self):
        """Can't find your result? Go check for the call log."""
        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.load_system_host_keys()
        client.connect(self.remote_server, username=self.remote_user, password=self.remote_password)
        command = 'grep "Address already in use." /var/mdta/log/{0}.log'.format(self.filename)
        print(command)
        stdin, stdout, stderr = client.exec_command(command)
        result_line = stdout.read()
        if result_line:
            return True
        return False

    def start_of_call(self, step):
        print("start_of_call: {0}".format(step))
        if step[:3].upper() == 'APN':
            self.apn = step[4:].strip()
        elif step[:4].upper() == 'DNIS':
            self.apn = step[5:].strip()
        elif step[:13].upper() == 'DIALEDNUMBER:':
            self.dialed_number = step[14:].strip()
        elif step[:4].upper() == 'DIAL':
            self.dialed_number = step[5:].strip()
        assert (len(self.body) == 0)
        self.body = 'IGNORE answer asr_session document_dump document_transition fetch grammar_activation license ' + \
                    'log note prompt recognition_start nuance recognition_end redux severe sip_session system_response ' + \
                    'transfer_start transfer_end vxml_event vxml_trace warning\n' + \
                    'EXPECT call_start\n'

    def dtmf_step(self, step):
        self.body += 'EXPECT recognition_start\nPAUSE 1\nDTMF ' + step[6:] + '\n'

    def no_input(self, step):
        self.body += 'EXPECT recognition_end\n'

    def end_of_call(self):
        """Previously used to append ENDCALL. Todo: refactor out"""
        pass

    def sip_string(self):
        if self.dialed_number:
            return 'sip:999000017{0}@{1}:5060'.format(self.dialed_number, self.sonus_server)
        else:
            return 'sip:{0}@{1}:5060'.format(self.apn, self.holly_server)


def bulk_remote_hat_execute(case_list):
    filename_list = []
    hat_script_list = NamedTemporaryFile(mode='wt', prefix='HAT', delete=False)
    for case in case_list:
        case.generate_hat_script()
        f = case.script._send_hat_script()
        filename_list.append(f)
        hat_script_list.write('destination: {0}\nscript: {1}\n'.format(case.script.sip_string(), f))
    hat_script_list.close()
    transport = Transport(case_list[0].script.remote_server, 22)
    transport.connect(username=case_list[0].script.remote_user,
                      password=case_list[0].script.remote_password)
    file_client = SFTPClient.from_transport(transport)
    file_client.put(hat_script_list.name, hat_script_list.name)
    file_client.close()

    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())
    client.load_system_host_keys()
    client.connect(case_list[0].script.remote_server,
                   username=case_list[0].script.remote_user,
                   password=case_list[0].script.remote_password)
    command = 'nohup hat -P {0} -p {1} -i /var/mdta/report/ -o /var/mdta/log{0}.log -b {2}:4080'.format(
        hat_script_list.name, case_list[0].script.sip_string(), case_list[0].script.holly_server)
    print(command)
    f = open('/home/caheyden/last-hat-command', 'w')
    f.write(command)
    f.close()
    conn = client.exec_command(command)
    time.sleep(50)  # Why? Don't know. Kinda don't care anymore. It runs better when it's here.
    client.close()
    return filename_list


def bulk_hatit_file_generator(case_list):
    csv_filename = 'hatit_{0}.csv'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    path = base.TMP_DIR
    if not os.path.exists(path):
        os.mkdir(path)
    with open(os.path.join(path, csv_filename), 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['everything', 'id'])
        for case in case_list:
            case.generate_hat_script()
            csv_writer.writerow([case.script.body, "{0}: {1}".format(case.id, case.title)])


    return csv_filename



