from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth import get_backends
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import UserResetForm, CustomPasswordChangeForm
from allauth.socialaccount.models import SocialAccount
from trips.models import Trip

@login_required
def reset_user_view(request):
    is_social_user = request.user.socialaccount_set.exists()
    can_change_password = request.user.has_usable_password()

    user_form = UserResetForm(instance=request.user)
    password_form = CustomPasswordChangeForm(user=request.user) if can_change_password else None

    if request.method == 'POST':
        user_form = UserResetForm(request.POST, instance=request.user)
        if can_change_password:
            password_form = CustomPasswordChangeForm(user=request.user, data=request.POST)

        valid = user_form.is_valid()
        if can_change_password:
            valid = valid and password_form.is_valid()

        if valid:
            user_form.save()
            if can_change_password:
                password_form.save()
                update_session_auth_hash(request, request.user)
            return redirect('profile')

    return render(request, 'users/reset_user.html', {
        'user_form': user_form,
        'password_form': password_form,
        'is_social_user': is_social_user,
        'can_change_password': can_change_password,
    })

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            backend = get_backends()[0]  # Default to first backend
            login(request, user, backend=backend.__class__.__module__ + "." + backend.__class__.__name__)

            return redirect('trip_list')  # or wherever you want to go
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def spotlight_view(request):
    return render(request, 'users/spotlight.html')

@login_required
def profile_view(request):
    recent_trips = (
        Trip.objects
            .filter(user=request.user)
            .order_by('-start_date')
            [:3]
    )

    context = {
        'recent_trips': recent_trips,
    }

    return render(request, 'users/profile.html', context)