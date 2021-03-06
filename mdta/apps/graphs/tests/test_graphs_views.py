from itertools import chain
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from mdta.apps.users.models import HumanResource
from mdta.apps.projects.models import Project


class GraphsViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        user_account = {
            'username': 'UserAccount',
            'password': 'UserPassword'
        }
        self.user = User.objects.create_user(
            username=user_account['username'],
            password=user_account['password']
        )

        self.project = Project.objects.create(
            name='H_testproject'
        )

        self.hr = HumanResource.objects.create(
            user=self.user,
            project=self.project
        )

    def test_home_without_fake_user_details(self):
        self.client.login(username= 'username', password='password')
        response = self.client.get(reverse('graphs:projects_for_selection'))
        self.assertEqual(response.status_code, 302)
        self.client.login(username= '', password='')
        response = self.client.get(reverse('graphs:projects_for_selection'))
        self.assertEqual(response.status_code, 302)

    def test_projects_for_selection(self):
        self.client.login(username='UserAccount', password='UserPassword')
        response = self.client.get(reverse('graphs:projects_for_selection'))
        self.assertEqual(response.status_code, 200)
        projects = list(chain.from_iterable(response.context['projects']))
        self.assertTrue(self.project in projects)

    def test_to_project_detail(self):
        self.client.login(username='UserAccount', password='UserPassword')
        response = self.client.get('/mdta/graphs/project_detail/'+str(self.hr.project.id)+'/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.project, response.context['project'])

    def test_graphs_with_login(self):
        self.client.login(username='UserAccount', password='UserPassword')
        response = self.client.get('/mdta/graphs/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.project in response.context['projects'])

    def test_graphs_without_login(self):
        response = self.client.get('/mdta/graphs/')
        self.assertRedirects(response,'/mdta/?next=/mdta/graphs/',status_code=302, target_status_code=200)


#    def test_redirection_to_project_detail_not_as_HR(self):
#        self.client.login(username= 'UserAccount', password='UserPassword')
#        response = self.client.get('graphs:project_detail/'+str(self.hr.project.id), follow=True)
#        self.assertEqual(response.status_code, 404)

#    def test_redirection_to_project_detail_as_HR(self):
#        self.client.login(username= 'UserAccount', password='UserPassword')
#        response = self.client.get('/mdta/graphs/project_detail/'+str(self.hr.project.id))
#        self.assertEqual(response.status_code, 200)



