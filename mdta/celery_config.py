from celery.schedules import crontab

# Celery config
CELERY_ACCEPT_CONTENT = ['pickle', 'json', ]
# CELERY_ENABLE_UTC = False
CELERY_RESULT_BACKEND = 'rpc://'
CELERY_RESULT_PERSISTENT = True
CELERY_RESULT_SERIALIZER = 'pickle'
CELERY_TASK_RESULT_EXPIRES = None   # no result is return back

CELERY_TIMEZONE = 'America/Chicago'

CELERY_ROUTES = {
    'mdta.apps.testcases.tasks.create_testcases': {'queue': 'mdta_queue'},
}

