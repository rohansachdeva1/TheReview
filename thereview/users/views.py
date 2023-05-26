from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django import forms
from .forms import RegisterForm, ProfilePicForm
from .models import Profile
from django.contrib import messages

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            pic = form.cleaned_data['profile_picture']

            user = authenticate(username=username, password=password)
            
            user.profile.email = email
            user.profile.profile_image = pic
            user.profile.save()
            
            
            login(request, user)
            return redirect('homepage')
    else:
        form = RegisterForm() # user creation form og

    return render(request, 'users/register.html', {'form': form})

def log_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            return redirect('login')
    
    return render(request, 'users/login.html')

def log_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('homepage')
    
def view_profile(request):
    return render(request, 'users/view_profile.html', {'user':request.user})

def update_profile(request):
    return render(request, 'users/view_profile.html', {'user':request.user})