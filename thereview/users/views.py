from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from django.contrib.auth import login, logout
from .forms import SignUpForm

# Create your views here.
def sign_up(request):
    if request.method == 'POST':
        # form = UserCreationForm(request.POST)
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            #create a user object from the user model - input all the data
            login(request, user)
            return redirect('homepage')
    # if post request - create this user, save em in the database, log them in, redirect them to the homewage
    else:
        form = SignUpForm() # user creation form og

    return render(request, 'users/signup.html', {'form': form})

def log_in(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('homepage')
    else:
        form = AuthenticationForm()
    
    return render(request, 'users/login.html', {'form':form})

def log_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('homepage')
    
def view_profile(request):
    return render(request, 'users/view_profile.html', {'user':request.user})