from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from mdta.apps.users.models import HumanResource
from django.shortcuts import render, redirect, get_object_or_404
from mdta.apps.projects.models import Project
from mdta.apps.graphs.utils import EDGE_TYPES_INVISIBLE_KEY

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
        project = self.project
        )


    def test_home_without_fake_user_details(self):
        self.client.login(username= 'username', password='password')
        response = self.client.get(reverse('graphs:projects_for_selection'))
        self.assertEqual(response.status_code, 302)
        self.client.login(username= '', password='')
        response = self.client.get(reverse('graphs:projects_for_selection'))
        self.assertEqual(response.status_code, 302)

    def test_projects_for_selection(self):
        self.client.login(username= 'UserAccount', password='UserPassword')
        response = self.client.get(reverse('graphs:projects_for_selection'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.project in response.context['projects'])

    def test_to_project_detail(self):
        self.client.login(username= 'UserAccount', password='UserPassword')
        response = self.client.get('/mdta/graphs/project_detail/'+str(self.hr.project.id)+'/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.project, response.context['project'])

    def test_graphs_without_login(self):
        response = self.client.get('/mdta/graphs/')
        self.assertRedirects(response,'/mdta/?next=/mdta/graphs/',status_code=302, target_status_code=200)





