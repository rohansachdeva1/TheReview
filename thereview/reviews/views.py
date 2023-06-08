from django.shortcuts import get_object_or_404, redirect, render
from .forms import ReviewForm
from django.contrib.auth.models import User
from content.models import Entity, Tag, Category
from .models import Review
from django.core.exceptions import ObjectDoesNotExist
import json

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

            review.save() # save new review
            return redirect('view_profile')
        else:
            return render(request, 'reviews/write_review.html', context)
    else:
        redirect('login')

# we know the user because their signed in
# we'll know the entity, because the user clicked on that to get here
# send the user a review form, link to currently signed in user and
# to the entity they clicked on. When they submit -> entity needs to
# be updated, profile preferences need to be updated, review needs to
# be saved to the profile