from django.shortcuts import redirect, render
from django.conf import settings

ACTIVE_TAB_CONFIG = ['projects_for_selection', 'node_type', 'edge_type']


def landing(request):
    if request.user.is_authenticated():
        return redirect('home')
    return render(request, 'core/landing.html')


def get_active_top_link(request):
    if request.path.startswith(settings.LOGIN_URL + 'graphs'):
        for item in ACTIVE_TAB_CONFIG:
            if item in request.path:
                active = 'config'
                break
        else:
            active = 'home'
    elif request.path.startswith(settings.LOGIN_URL + 'projects'):
        active = 'config'
    elif request.path.startswith(settings.LOGIN_URL + 'testcases'):
        if 'testrail' not in request.path:
            active = 'testcases'
        else:
            active = 'config'
    elif request.path.startswith(settings.LOGIN_URL + 'help'):
        active = 'help'
    else:
        active = 'mdta'

    return {'active': active}
