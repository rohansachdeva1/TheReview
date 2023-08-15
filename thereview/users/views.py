from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db.models import Sum
from users.models import UserTag
from content.models import Entity
from .forms import RegisterForm
from reviews.models import Review
from django.db import models
import random

# Register new users using the custom Register form, authenticate them and log them in, no parameters
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
            user.profile.bio = bio

            # Check if pic is empty (None) or an empty file
            if not pic:
                # If no profile picture is uploaded, set it to one of 8 default image paths
                random_number = random.randint(1, 8)
                default_profile_pic = f'profile/default_pp_{random_number}.PNG'
                user.profile.profile_image = default_profile_pic
            else:
                # Otherwise, save the uploaded picture
                user.profile.profile_image = pic
            
            user.profile.save()
            
            login(request, user) # log user in using django contrib auth
            return redirect('homepage') # redirect back to homepage (now signed in)
    else:
        form = RegisterForm() # send empty custom register form

    return render(request, 'users/register.html', {'form': form}) # render register form

# Authenticate and log the user in, no parameters
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

# Log the user out, no parameters
def log_out(request):
    logout(request) # log current user out from request object
    return redirect('homepage') # redirect to homepage

# View user's profile, username parameter
def view_profile(request, username):
    user = get_object_or_404(User, id=request.user.id)
    profile_user = get_object_or_404(User, username=username)
    update_user(profile_user.id)

    # Get reviews, private or all depending if you are viewing another profile or your own
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

# Update user metrics like tags, reviewed, avg_rating, etc. User id parameter
def update_user(user_id):
    user = get_object_or_404(User, id=user_id)

    # update number of reviews and average rating
    user.profile.reviewed = Review.objects.filter(user=user).count() 
    user.profile.avg_rating = Review.objects.filter(user=user).aggregate(models.Avg('final_score')).get('final_score__avg')
    user.profile.save()

    # Update UserTag counts and sum_scores
    user_tags = UserTag.objects.filter(user=user)
    for user_tag in user_tags:
        tag = user_tag.tag
        user_tag.count = Review.objects.filter(user=user, tags=tag).count()
        user_tag.sum_scores = Review.objects.filter(user=user, tags=tag).aggregate(total_score=Sum('final_score')).get('total_score', 0)
        user_tag.save()

# Follow user, user id parameter
def follow(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)

    # Check that they are already following profile user, add to follows
    if (request.user.profile not in profile_user.profile.followed_by.all()):
        request.user.profile.follows.add(profile_user.profile)

    return redirect('view_profile', profile_user.username)

# Unfollow user, user id parameter
def unfollow(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)

    # Check that they are already following profile user, remove from follows
    if (request.user.profile in profile_user.profile.followed_by.all()):
        request.user.profile.follows.remove(profile_user.profile)

    return redirect('view_profile', profile_user.username) # redirect to profile page

# Seen Functionality
def seen(request, entity_id):
    entity = get_object_or_404(Entity, id=entity_id)

    # Check if the entity is in the user's seen section
    if entity in request.user.profile.seen.all():
        request.user.profile.seen.remove(entity)
    else:
        request.user.profile.seen.add(entity)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

# Edit Bio Functionality
def edit_bio(request):
    if request.method == "POST":
        new_bio = request.POST.get('new_bio', '')
        user = get_object_or_404(User, id=request.user.id)
        user.profile.bio = new_bio
        user.profile.save()
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

# Edit Profile Picture Functionality
def edit_profile_image(request):
    if request.method == "POST":
        user = get_object_or_404(User, id=request.user.id)
        
        profile_image = request.FILES.get('profile_image')
        if profile_image:
            user.profile.profile_image = profile_image
            user.profile.save()
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))