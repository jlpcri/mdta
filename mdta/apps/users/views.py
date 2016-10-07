from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from mdta.apps.users.models import HumanResource


def user_is_superuser(user):
    return user.is_superuser


def user_is_staff(user):
    return user.is_staff


@login_required
def mdta(request):
    return render(request, 'users/mdta.html')


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


@user_passes_test(user_is_superuser)
def user_management(request):
    if request.method == 'GET':
        sort_types = [
            'username',
            '-username',
            'first_name',
            '-first_name',
            'last_login',
            '-last_login',
        ]
        users = ''
        sort = request.GET.get('sort', '')
        sort = sort if sort else 'username'

        if sort in sort_types:
            users = User.objects.order_by(sort)

        context = {
            'users': users,
            'sort': sort,
        }

        return render(request, 'users/user_management.html', context)


@user_passes_test(user_is_superuser)
def user_update(request, user_id):
    if request.method == "POST":
        user = get_object_or_404(User, pk=user_id)

        user.is_active = request.POST.get('is_active', False) \
            or request.POST.get('is_staff', False) \
            or request.POST.get('is_superuser', False)
        user.is_staff = request.POST.get('is_staff', False)
        user.is_superuser = request.POST.get('is_superuser', False)

        user.save()

        return redirect('users:management')
    else:
        return redirect('users:management')