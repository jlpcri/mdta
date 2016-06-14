from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.core.urlresolvers import resolve, reverse


from mdta.apps.core.views import landing


class CoreViewsTest(TestCase):
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

    def test_landing_url_resolve_to_view(self):
        found = resolve(reverse('landing'))
        self.assertEqual(found.func, landing)

    def test_landing_return_200(self):
        response = self.client.get(reverse('landing'))
        self.assertEqual(response.status_code, 200)

    def test_landing_without_authenticated(self):
        response = self.client.get(reverse('landing'))
        self.assertContains(response, 'Please use your Active Directory credentials.')

    def test_landing_with_authenticated(self):
        self.client.login(
            username=self.user_account['username'],
            password=self.user_account['password']
        )
        response = self.client.get(reverse('landing'), follow=True)
        self.assertNotContains(response, 'Please use your Active Directory credentials.')
        self.assertContains(response, '<li><a href="/mdta/projects/"><i class="fa fa-sitemap fa-fw"></i> Projects</a> </li>')
        self.assertContains(response, '<li><a href="/mdta/graphs/"><i class="fa fa-automobile fa-fw"></i> Graphs</a> </li>')
        self.assertContains(response, '<li><a href="/mdta/help/"><i class="fa fa-thumbs-o-up"></i> Help</a> </li>')

