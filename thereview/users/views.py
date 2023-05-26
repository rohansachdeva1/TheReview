from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .forms import UpdateForm
from .models import Profile
from django.contrib import messages

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('homepage')
    else:
        form = UserCreationForm() # user creation form og

    return render(request, 'users/signup.html', {'form': form})

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

def log_in2(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        


def log_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('homepage')
    
def view_profile(request):
    return render(request, 'users/view_profile.html', {'user':request.user})

def update_profile(request):
    current_user = User.objects.get(id=request.user.id)
    form = UpdateForm(request.POST or None, instance=current_user)

    return render(request, 'users/update_profile.html', {'form':form})