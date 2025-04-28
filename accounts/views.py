from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import update_session_auth_hash
from .forms import (
    CustomUserCreationForm, 
    CustomUserChangeForm, 
    CustomPasswordChangeForm
)
from .models import CustomUser

def user_login(request):
     if request.method == 'POST':
        form = AuthenticationForm(request=request, data = request.POST)
        if form.is_valid():
           messages.success(request,' Login successfully!!!')
           name = form.cleaned_data['username']
           userpass = form.cleaned_data['password']
           user = authenticate(username = name,password = userpass)
           if user is not None:
              login(request,user)
              return redirect('profile')
     else:
        form = AuthenticationForm()
    
     return render(request, 'accounts/login.html')
 
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')

@login_required
def profile(request, username=None):
    if username:
        profile_user = CustomUser.objects.get(username=username)
    else:
        profile_user = request.user
    
    posts = profile_user.post_set.all().order_by('-created_at')
    return render(request, 'accounts/profile.html', {
        'profile_user': profile_user,
        'posts': posts
    })

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(
            request.POST, 
            request.FILES, 
            instance=request.user
        )
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    
    return render(request, 'accounts/profile_edit.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
    else:
        form = CustomPasswordChangeForm(request.user)
    
    return render(request, 'accounts/change_password.html', {'form': form})