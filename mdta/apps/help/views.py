from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


@login_required
def help(request):
    help_url = 'https://wiki.west.com/display/QE/MDTA'
    return redirect(help_url)
