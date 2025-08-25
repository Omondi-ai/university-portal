from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import UserRegisterForm, UserUpdateForm, ApplicationForm
from .models import User, Application
from departments.models import Department

def home_view(request):
    context = {
        'departments': Department.objects.all(),
        'online_users': User.objects.filter(is_online=True) if request.user.is_authenticated else []
    }
    return render(request, 'home.html', context)
    
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            
            # Handle department assignment based on role
            if user.role == User.VISITOR:
                user.department = None  # Visitors don't have departments
            elif user.role == User.STUDENT and not user.department:
                # Set a default department for students if none selected
                default_dept = Department.objects.first()
                if default_dept:
                    user.department = default_dept
                    messages.info(request, f'You have been assigned to {default_dept.name} department.')
            
            user.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegisterForm()
    
    return render(request, 'accounts/register.html', {
        'form': form,
        'departments': Department.objects.all()
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            user.is_online = True
            user.save()
            messages.success(request, f'Welcome back {username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'accounts/login.html')

@login_required
def logout_view(request):
    request.user.is_online = False
    request.user.save()
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})

@login_required
def password_change_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/password_change.html', {'form': form})

def application_view(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.save()
            messages.success(request, 'Your application has been submitted successfully!')
            return redirect('home')
    else:
        form = ApplicationForm()
    return render(request, 'accounts/application.html', {'form': form})