from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect

from tanks.forms import BalanceForm
from tanks.models import Tank, TankSale
from .forms import RegistrationForm, LoginForm


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'authenticate/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'authenticate/login.html', {'form': form})


def home(request):
    tanks = Tank.objects.all()

    return render(request, 'home.html', {'tanks': tanks})


def logout_view(request):
    logout(request)
    return redirect('login')


from django.contrib.auth import update_session_auth_hash
from .forms import UserChangeForm, UserPasswordChangeForm


def user_profile(request):
    all_tanks = Tank.objects.all()
    my_tanks = Tank.objects.filter(owner=request.user)

    if request.method == 'POST':
        balance_form = BalanceForm(request.POST)
        user_change_form = UserChangeForm(request.POST, instance=request.user)
        password_change_form = UserPasswordChangeForm(request.user, request.POST)

        if balance_form.is_valid():
            amount = balance_form.cleaned_data['amount']
            request.user.balance += amount
            request.user.save()
            return redirect('profile')

        if user_change_form.is_valid() and password_change_form.is_valid():
            user_change_form.save()
            password_change_form.save()
            update_session_auth_hash(request, password_change_form.user)
            return redirect('profile')
    else:
        user_change_form = UserChangeForm(instance=request.user)
        password_change_form = UserPasswordChangeForm(request.user)
        balance_form = BalanceForm()
    return render(request, 'authenticate/profile.html', {
        'all_tanks': all_tanks,
        'my_tanks': my_tanks,
        'user_change_form': user_change_form,
        'password_change_form': password_change_form,
        'balance_form': balance_form
    })
