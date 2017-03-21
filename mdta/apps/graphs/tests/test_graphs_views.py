from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.core.urlresolvers import resolve, reverse
from mdta.apps.graphs.views import graphs
from mdta.apps.users.models import HumanResource

class GraphsViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user_account = {
            'username': 'UserAccount',
            'password': 'UserPassword'
        }
        self.user = User.objects.create_user(
            username=self.user_account['username'],
            password=self.user_account['password']
        )
        self.hr = HumanResource.objects.create(
            user=self.user
        )
    def test_landing_return_200(self):
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, '/mdta/?next=/mdta/home/', 302, 200)

    def test_login(self):
        self.client.login(
            username=self.user_account['username'],
            password=self.user_account['password']
        )
        response = self.client.get(reverse('home'), follow=True)
        self.assertNotContains(response, 'Please use your Active Directory credentials.')

    def test_graph_page_with_new_user(self):
        self.client.login(
            username=self.user_account['username'],
            password=self.user_account['password']
        )
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, '/mdta/graphs/projects_for_selection/', 302, 200)

    