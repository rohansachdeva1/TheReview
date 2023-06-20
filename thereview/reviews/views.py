from django.shortcuts import get_object_or_404, redirect, render
from .forms import ReviewForm
from django.contrib.auth.models import User
from content.models import Entity, Tag, Category
from .models import Review
from django.core.exceptions import ObjectDoesNotExist
import json
from django.urls import reverse
from django.db import models
from content.views import update_entity

# Create your views here.
def write_review(request, entity_id):
    
    # Store core data in local variables from request object
    entity = get_object_or_404(Entity, id=entity_id)
    medium = entity.medium
    tags = Tag.objects.filter(medium=medium)
    categories = Category.objects.filter(medium=medium)
    user = get_object_or_404(User, id=request.user.id)

    # store data to be used in write_review template in context
    context = {
        'entity': entity,
        'tags': tags,
        'categories': categories,
        # ... other context data ...
    }

    if request.user.is_authenticated:
        if request.method == "POST":
            final_score = request.POST.get('final_score') # get final_score from form
            blurb = request.POST.get('blurb') # get blurb from form
            
            # create new review and populate it with required data
            review = Review(user=user, entity=entity, final_score=final_score, blurb=blurb)
            review.save()

            # get privacy toggle from form
            if request.POST.get("make_private") == "private":
                review.private = True
            else:
                review.private = False

            # get categories data from form
            i = 1
            while f'feedback_{i}' in request.POST:
                category_name = request.POST[f'category_{i}']
                feedback = request.POST.get(f'feedback_{i}', '')
                
                # update review object
                category_rating = f'category_rating{i}'
                if feedback == 'like':
                    setattr(review, category_rating, 1)
                elif feedback == 'dislike':
                    setattr(review, category_rating, -1)

                i += 1 # increment counter

            # get tag data from form
            # Loop through the form data and retrieve the values of the selected tags
            for key in request.POST.keys():
                if key.startswith('tag_'):
                    tag_id = request.POST[key]
                    if tag_id.isdigit():
                        tag = Tag.objects.get(id=int(tag_id))
                        review.tags.add(tag) # added tags to review object
            
            # Update Entity
            update_entity(entity.id)

            review.save() # save new review
            
            view_profile_url = reverse('view_profile', args=[user.username])
            return redirect(view_profile_url)
        
        else:
            return render(request, 'reviews/write_review.html', context)
        
    else:
        redirect('login')

def view_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    # store data to be used in view_review template in context
    context = {
        'review': review,
        # ... other context data ...
    }

    return render(request, 'reviews/review_detail.html', context)

def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)


    review.delete()
    user = get_object_or_404(User, id=request.user.id)

    view_profile_url = reverse('view_profile', args=[user.username])
    return redirect(view_profile_url)