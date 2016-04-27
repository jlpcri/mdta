from django.shortcuts import redirect, render


def landing(request):
    if request.user.is_authenticated():
        return redirect('users:home')
    return render(request, 'core/landing.html')
