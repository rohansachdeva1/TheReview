from django.http import HttpResponse
from django.shortcuts import render
from .models import Entity
import requests
from content.models import Medium

# Create your views here.
def search_query(request):
    return render(request, 'content/search_bar.html')

def search_entities(request):
    if request.method == "POST":
        user_input = request.POST['searched'] # try paren setting a new 'searched' variable equal to the search query from user
        results = Entity.objects.filter(title__icontains=user_input)

        if results.count() < 5:
            response = requests.get('https://imdb-api.com/en/API/SearchMovie/k_28nyce3o/' + user_input)
            data = response.json()
            for item in data['results']:
                title = item['title']
                image = item['image']
                description = item['description']

                medium = Medium.objects.get(name='Other')  # Default medium value for cases without resultType
                if 'resultType' in item and item['resultType'] == "Movie":
                    medium = Medium.objects.get(name='Movies')

                if (not Entity.objects.filter(description=description)):
                    entity_obj = Entity.objects.create(title=title, image=image, description=description, medium=medium)
                    entity_obj.save()    

            new_results = Entity.objects.filter(title__icontains=user_input)
            return render(request, 'content/search_results.html', {'results': new_results})
        
        else:
            return render(request, 'content/search_results.html', {'results': results})
    #query = request.GET.get('query')
    #results = Entity.objects.filter(title__icontains=query)
    #return render(request, 'content/search_results.html', {'results': results})