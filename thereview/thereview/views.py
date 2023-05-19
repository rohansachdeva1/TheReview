from django.http import HttpResponse
from django.shortcuts import render

def homepage(request):
    return render(request, 'homepage.html')

def search_movie(request):
    # get the data from api or db
    return render(request, 'search_bar.html')