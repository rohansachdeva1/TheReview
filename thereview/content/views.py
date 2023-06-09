from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Entity
import requests
from content.models import Medium

# Create your views here.

def search_entities(request):
    if request.method == "POST":
        request.session['search_page_url'] = request.get_full_path()
        user_input = request.POST['searched']
        
        results = Entity.objects.filter(title__icontains=user_input)[:12]

        # use api if not enough objects in database (10)
        if results.count() < 12:
            data = requests.get('https://imdb-api.com/en/API/SearchMovie/k_28nyce3o/' + user_input).json()

            # loop through json object and create variables for needed fields
            for item in data['results']:
                id = item['id']
                title = item['title']
                slug = title.replace(' ', '-').lower()
                image = item['image']
                description = item['description']

                medium = Medium.objects.get(name='Other')  # Default medium value for cases without resultType
                if 'resultType' in item and item['resultType'] == "Movie":
                    medium = Medium.objects.get(name='Movies')

                # prevent duplicates by checking if description is different, create new entity object and save
                if (not Entity.objects.filter(description=description)):
                    entity_obj = Entity.objects.create(api_id=id, slug_field=slug, title=title, image=image, description=description, medium=medium)

            # now query the updated database and return new results in search results template
            new_results = Entity.objects.filter(title__icontains=user_input)[:12]
            return render(request, 'content/search_tile_results.html', {'results': new_results})
        
        # return original list from database if results more than 10
        else:
            return render(request, 'content/search_tile_results.html', {'results': results})
    else:
        return redirect('homepage')

def view_entity(request, entity_id):
    entity = get_object_or_404(Entity, id=entity_id)

    context = {
        'entity': entity,
        # ... other context data ...
    }
    
    return render(request, 'content/entity_detail.html', context)