from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from mdta.apps.users.models import HumanResource
from mdta.apps.core.views import landing

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
        response = self.client.get(reverse('graphs'))
        self.assertEqual(response.status_code, 200)

    def test_login_required(self):
        response = self.client.get(reverse('landing'))
        self.assertContains(response, 'Please use your Active Directory credentials.')

