from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def help(request):
    return render(request, 'help/help.html')
