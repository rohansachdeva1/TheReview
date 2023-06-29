from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db.models import Sum
from users.models import UserTag
from .forms import RegisterForm
from reviews.models import Review
from django.db import models

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
            update_user(user.id)
            return redirect('homepage')
        # if not, prompt them to log in again
        else:
            return redirect('login')
    
    return render(request, 'users/login.html') # render the login template

def log_out(request):
    logout(request) # log current user out from request object
    return redirect('homepage') # redirect to homepage
    
def view_profile(request, username):
    user = get_object_or_404(User, id=request.user.id)
    profile_user = get_object_or_404(User, username=username)
    update_user(profile_user.id)
    try:
        if user == profile_user:
            # Current user is the profile user, show all reviews
            reviews = Review.objects.filter(user=profile_user).order_by("-created_at")
        else:
            # Current user is not the profile user, show only non-private reviews
            reviews = Review.objects.filter(user=profile_user, private=False).order_by("-created_at")

    except Review.DoesNotExist:
        reviews = None

    context = {
        'user': profile_user,
        'reviews': reviews,
        # ... other context data ...
    }

    return render(request, 'users/view_profile.html', context)

def update_user(user_id):
    user = get_object_or_404(User, id=user_id)

    user.profile.reviewed = Review.objects.filter(user=user).count() # update number of reviews
    user.profile.avg_rating = Review.objects.filter(user=user).aggregate(models.Avg('final_score')).get('final_score__avg')
    user.profile.save()

    # Update UserTag counts and sum_scores
    user_tags = UserTag.objects.filter(user=user)
    for user_tag in user_tags:
        tag = user_tag.tag
        user_tag.count = Review.objects.filter(user=user, tags=tag).count()
        user_tag.sum_scores = Review.objects.filter(user=user, tags=tag).aggregate(total_score=Sum('final_score')).get('total_score', 0)
        user_tag.save()

def follow(request, user_id):
    request_user = get_object_or_404(User, id=request.user.id)
    user_to_follow = get_object_or_404(User, id=user_id)
    pass

def unfollow(request, user_id):
    pass