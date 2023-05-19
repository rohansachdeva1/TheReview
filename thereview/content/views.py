from django.http import HttpResponse
from django.shortcuts import render
from .models import Entity

# Create your views here.
def search_query(request):
    return render(request, 'content/search_bar.html')

def search_entities(request):
    if request.method == "POST":
        user_input = request.POST['searched'] # try paren setting a new 'searched' variable equal to the search query from user
        # query our db with the user_input -> list of all the results for user_input
        results = Entity.objects.filter(title__startswith=user_input)
        # search db with user_input
        # if not found make api call with user input
        # parse data from json s
        # return data in list view
        return render(request, 'content/search_results.html', {'results': results})
    else:
        return
    #query = request.GET.get('query')
    #results = Entity.objects.filter(title__icontains=query)
    #return render(request, 'content/search_results.html', {'results': results})