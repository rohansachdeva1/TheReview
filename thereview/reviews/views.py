from django.shortcuts import render

# Create your views here.
def review_builder(request):
    return render(request, 'reviews/review_builder.html')