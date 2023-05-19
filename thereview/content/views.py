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
        user_input = request.POST['searched']
        results = Entity.objects.filter(title__icontains=user_input)[:10]

        # use api if not enough objects in database (5)
        if results.count() < 5:
            response = requests.get('https://imdb-api.com/en/API/SearchMovie/k_28nyce3o/' + user_input)
            data = response.json()

            #Loop through json object and create variables for needed fields
            for item in data['results']:
                title = item['title']
                image = item['image']
                description = item['description']

                medium = Medium.objects.get(name='Other')  # Default medium value for cases without resultType
                if 'resultType' in item and item['resultType'] == "Movie":
                    medium = Medium.objects.get(name='Movies')
                
                # prevent duplicates by checking if description is different, create new entity object and save
                if (not Entity.objects.filter(description=description)):
                    entity_obj = Entity.objects.create(title=title, image=image, description=description, medium=medium)
                    entity_obj.save()    

            # now query the updated database and return new results in search results template
            new_results = Entity.objects.filter(title__icontains=user_input)[:10]
            return render(request, 'content/search_results.html', {'results': new_results})
        
        # return original list from database if results more than 5
        else:
            return render(request, 'content/search_results.html', {'results': results})