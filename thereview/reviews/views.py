from django.shortcuts import redirect, render

# Create your views here.
def write_review(request):
    return render(request, 'reviews/write_review.html')

# we know the user because their signed in
# we'll know the entity, because the user clicked on that to get here
# send the user a review form, link to currently signed in user and
# to the entity they clicked on. When they submit -> entity needs to
# be updated, profile preferences need to be updated, review needs to
# be saved to the profile