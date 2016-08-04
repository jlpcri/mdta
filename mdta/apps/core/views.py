from django.shortcuts import redirect, render
from django.conf import settings


def landing(request):
    if request.user.is_authenticated():
        return redirect('users:home')
    return render(request, 'core/landing.html')


def get_active_top_link(request):
    if request.path.startswith(settings.LOGIN_URL + 'projects'):
        active = 'projects'
    elif request.path.startswith(settings.LOGIN_URL + 'testcases'):
        active = 'projects'
    elif request.path.startswith(settings.LOGIN_URL + 'graphs'):
        active = 'graphs'
    elif request.path.startswith(settings.LOGIN_URL + 'help'):
        active = 'help'
    else:
        active = 'home'

    return {'active': active}
