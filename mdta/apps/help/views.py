from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.conf import settings

@login_required
def help(request):
    return redirect(settings.CONFLUENCE_LINK)
