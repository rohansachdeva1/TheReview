from django.shortcuts import get_object_or_404, redirect, render
from .forms import ReviewForm
from django.contrib.auth.models import User
from content.models import Entity, Tag, Category
from .models import Review

# Create your views here.
def write_review(request, entity_id):
    entity = get_object_or_404(Entity, id=entity_id)
    medium = entity.medium
    tags = Tag.objects.filter(medium=medium)
    categories = Category.objects.filter(medium=medium)
    user = get_object_or_404(User, id=request.user.id)

    context = {
        'entity': entity,
        'tags': tags,
        'categories': categories,
        # ... other context data ...
    }

    if request.user.is_authenticated:
        if request.method == "POST":
            #final_score = float(request.POST.get['final_score'])
            final_score = request.POST.get('final_score')
            print(final_score)
            blurb = request.POST.get('blurb')

            # create new review
            review = Review(user=user, entity=entity, final_score=final_score, blurb=blurb)

            if request.POST.get("make_private") == "private":
                review.private = True
            else:
                review.private = False
            
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