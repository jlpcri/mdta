from django.shortcuts import redirect, render
from django.conf import settings

ACTIVE_TAB_CONFIG = ['projects_for_selection', 'node_type', 'edge_type']


def landing(request):
    if request.user.is_authenticated():
        return redirect('home')
    return render(request, 'core/landing.html')

