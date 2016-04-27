from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from model_driven.apps.users.models import HumanResource


def home(request):
    return render(request, 'users/home.html')


def sign_in(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'],
                            password=request.POST['password'])
        if user:
            if user.is_active:
                login(request, user)
                try:
                    hr = HumanResource.objects.get(user=user)
                except HumanResource.DoesNotExist:
                    HumanResource.objects.create(user=user)
                if request.GET.get('next'):
                    return redirect(request.GET['next'])
                else:
                    return redirect('users:home')
            else:
                messages.error(request, 'This account is inactive')
        else:
            messages.error(request, 'Invalid username or password')

    return redirect('landing')


@login_required
def sign_out(request):
    logout(request)
    return redirect('landing')


def user_management(request):
    pass
