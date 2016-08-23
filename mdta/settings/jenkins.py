__author__ = 'sliu'
from mdta.settings.base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'test_mdta',
        'USER': 'scorecard',
        'PASSWORD': 'scorecard_development',
        'HOST': 'qaci01.wic.west.com',
        'PORT': '5433',
    }
}

INSTALLED_APPS += ('django_jenkins', )

PROJECT_APPS = (
    'mdta.apps.core',
    'mdta.apps.graphs',
    'mdta.apps.help',
    'mdta.apps.projects',
    'mdta.apps.users'
)

JENKINS_TASKS = (
    'django_jenkins.tasks.run_pylint',
)

TEST_COVERAGE_EXCLUDES_FOLDERS = [
    '/usr/local/*',
    'mdta/apps/*/tests/*',
]
