from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .forms import RegisterForm
from reviews.models import Review

# Create your views here.
def register(request):
    if request.method == 'POST': # once user has filled out form
        form = RegisterForm(request.POST, request.FILES)
        
        if form.is_valid(): # validate that form has been filled out correctly
            form.save()

            # take user entered data from the form and store it variables
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            pic = form.cleaned_data['profile_picture']
            bio = form.cleaned_data['bio']

            # authenticate form using django contrib auth
            user = authenticate(username=username, password=password)
            
            # save non-required fields to user's profile
            user.profile.email = email
            user.profile.profile_image = pic
            user.profile.bio = bio
            user.profile.save()
            
            login(request, user) # log user in using django contrib auth
            return redirect('homepage') # redirect back to homepage (now signed in)
    else:
        form = RegisterForm() # send empty custom register form

    return render(request, 'users/register.html', {'form': form}) # render register form

def log_in(request):
    if request.method == 'POST': # once user has filled our form
        username = request.POST['username'] # get username and password from request object
        password = request.POST['password']
        user = authenticate(request, username=username, password=password) # authenticate user
        
        # if the user exists, log them in and redirect to homepage
        if user is not None:
            login(request, user)
            return redirect('homepage')
        # if not, prompt them to log in again
        else:
            return redirect('login')
    
    return render(request, 'users/login.html') # render the login template

def log_out(request):
    logout(request) # log current user out from request object
    return redirect('homepage') # redirect to homepage
    
def view_profile(request, username):

    # get user from request object and send review data to template
    user = get_object_or_404(User, id=request.user.id)
    try:
        reviews = Review.objects.filter(user=user).order_by("-created_at")
    except Review.DoesNotExist:
        reviews = None

    return render(request, 'users/view_profile.html', {'user':user, 'reviews':reviews})