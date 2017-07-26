from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


@login_required
def help(request):
    # return render(request, 'help/help.html')
    help_url = 'https://wiki.west.com/display/QE/MDTA'
    return redirect(help_url)
