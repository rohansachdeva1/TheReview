from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from content.models import Entity, Tag, Category, EntityTag
from users.models import UserTag
from .models import Review
from django.urls import reverse
from django.db import models
from content.views import update_entity
from users.views import update_user
from django.http import HttpResponseRedirect

# Write a review, entity id parameter, (linked to a user and an entity)
def write_review(request, entity_id):
    
    # Store core data in local variables from request object
    entity = get_object_or_404(Entity, id=entity_id)
    medium = entity.medium
    tags = Tag.objects.filter(medium=medium)
    categories = Category.objects.filter(medium=medium)
    user = get_object_or_404(User, id=request.user.id)

    # Store data to be used in write_review template in context
    context = {
        'entity': entity,
        'tags': tags,
        'categories': categories,
        # ... other context data ...
    }

    # Create and populate new review object and save to profile
    if request.user.is_authenticated:
        if request.method == "POST":
            final_score = request.POST.get('final_score') # get final_score from form
            blurb = request.POST.get('blurb') # get blurb from form
            
            # Create new review and populate it with required data
            review = Review(user=user, entity=entity, final_score=final_score, blurb=blurb)
            review.save()

            # Get privacy toggle from form
            if request.POST.get("make_private") == "private":
                review.private = True
            else:
                review.private = False

            # Get categories data from form
            i = 1
            while f'feedback_{i}' in request.POST:
                category_name = request.POST[f'category_{i}']
                feedback = request.POST.get(f'feedback_{i}', '')
                
                category_rating = f'category_rating{i}'
                if feedback == 'like':
                    setattr(review, category_rating, 1)
                elif feedback == 'dislike':
                    setattr(review, category_rating, -1)

                i += 1 # increment counter

            # Get tag data from form
            # Loop through the form data and retrieve the values of the selected tags
            for key in request.POST.keys():
                if key.startswith('tag_'):
                    tag_id = request.POST[key]
                    if tag_id.isdigit():
                        tag = Tag.objects.get(id=int(tag_id))
                        review.tags.add(tag) # added tags to review object

                        # Add tags to entity
                        try:
                            entity_tag = EntityTag.objects.get(entity=entity, tag=tag)
                            entity_tag.count += 1
                            entity_tag.save()
                        except EntityTag.DoesNotExist:
                            entity_tag = EntityTag(entity=entity, tag=tag, count=1)
                            entity_tag.save()

                        # Add tags to user profile
                        try:
                            user_tag = UserTag.objects.get(user=user, tag=tag)
                            user_tag.count += 1
                            if user_tag.sum_scores is not None:
                                user_tag.sum_scores += float(review.final_score)
                            else:
                                user_tag.sum_scores = float(review.final_score)
                            user_tag.save()
                        except UserTag.DoesNotExist:
                            user_tag = UserTag(user=user, tag=tag, count=1, sum_scores=review.final_score)
                            user_tag.save()               
            
            # Update entity and user metrics
            update_entity(entity.id)
            update_user(user.id)

            review.save() # save new review
            
            view_profile_url = reverse('view_profile', args=[user.username])
            return redirect(view_profile_url)
        
        else:
            return render(request, 'reviews/write_review.html', context)
        
    else:
        return redirect('homepage')

# View review in review detail page, review id parameter
def view_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    full_stars = int(review.final_score)
    half_star_value = review.final_score - full_stars

    # store data to be used in view_review template in context
    context = {
        'review': review,
        'full_stars': full_stars,
        'half_star_value': half_star_value,
        # ... other context data ...
    }

    return render(request, 'reviews/review_detail.html', context)

# Delete a review from profile, review id parameter
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    review.delete()

    update_entity(review.entity.id)
    update_user(review.user.id)

    view_profile_url = reverse('view_profile', args=[review.user.username])
    return redirect(view_profile_url)

# Like or unlike review, review id parameter
def like_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    review_user = get_object_or_404(User, id=review.user.id)
    request_user = get_object_or_404(User, id=request.user.id)

    # check if they already like the post
    if review.likes.filter(username=request_user.username):
        review.likes.remove(request_user)
    else:
        review.likes.add(request_user)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

# Edit review blurb, review id parameter
def edit_blurb(request, review_id):
    if request.method == "POST":
        new_blurb = request.POST.get('new_blurb', '')
        review = get_object_or_404(Review, id=review_id)
        review.blurb = new_blurb
        review.save()
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def comment_review(request, review_id):
    pass