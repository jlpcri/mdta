from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.core.urlresolvers import resolve, reverse
from mdta.apps.graphs.views import graphs
from mdta.apps.users.models import HumanResource
from mdta.apps.projects.models import Project

class GraphsViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user_account_1 = {
            'username': 'UserAccount1',
            'password': 'UserPassword1',
        }
        self.user_account_2 = {
            'username': 'UserAccount2',
            'password': 'UserPassword2',
        }
        self.user1 = User.objects.create_user(
            username=self.user_account_1['username'],
            password=self.user_account_1['password']
        )
        self.user2 = User.objects.create_user(
            username=self.user_account_2['username'],
            password=self.user_account_2['password']
        )
        self.hr1 = HumanResource.objects.create(
            user=self.user1
        )
        self.hr2 = HumanResource.objects.create(
            user=self.user2
        )
    def test_landing_return_200(self):
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, '/mdta/?next=/mdta/home/', 302, 200)

    def test_login(self):
        self.client.login(
            username=self.user_account_1['username'],
            password=self.user_account_1['password']
        )
        response = self.client.get(reverse('home'), follow=True)
        self.assertNotContains(response, 'Please use your Active Directory credentials.')

    def test_graph_page_with_new_user(self):
        self.client.login(
            username=self.user_account_1['username'],
            password=self.user_account_1['password']
        )
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, '/mdta/graphs/projects_for_selection/', 302, 200)

    def test_graph_page_with_established_user(self):
        self.project = Project.objects.create(
            name = 'mdta_project'
        )
        self.hr_project = HumanResource.objects.create(
            project=self.project
        )
        self.client.login(
            username=self.user_account_2['username'],
            password=self.user_account_2['password']
        )
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, '/mdta/graphs/project_detail/', 302, 200)


