from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def graphs(request):
    return render(request, 'graphs/graphs.html')
