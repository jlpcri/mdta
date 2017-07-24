from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.conf import settings


@login_required
def help(request):
    if request.user.username == 'sliu':
        return render(request, 'help/help.html')
    return redirect(settings.CONFLUENCE_LINK)
