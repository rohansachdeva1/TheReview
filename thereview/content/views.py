from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
import requests
from content.models import Medium, Entity, EntityTag
from reviews.models import Review
from django.dispatch import receiver
from reviews.signals import review_saved
from reviews.signals import review_deleted
from django.db import models


# Create your views here.

def search_entities(request):
    if request.method == "POST":
        request.session['search_page_url'] = request.get_full_path()
        user_input = request.POST['searched']
        
        results = Entity.objects.filter(title__icontains=user_input)[:12]

        # use api if not enough objects in database (10)
        if results.count() < 12:
            data = requests.get('https://imdb-api.com/API/AdvancedSearch/k_28nyce3o?title=' + user_input).json()

            # loop through json object and create variables for needed fields
            for item in data['results']:
                id = item['id']
                title = item['title']
                slug = title.replace(' ', '-').lower()
                image = item['image']
                description = item['description']
                plot = item['plot']

                medium = Medium.objects.get(name='Movies')  # Default medium value for cases without resultType

                # prevent duplicates by checking if description is different, create new entity object and save
                if (not Entity.objects.filter(description=description)):
                    entity_obj = Entity.objects.createentity_obj = Entity.objects.create(
                        api_id=id, 
                        slug_field=slug, 
                        title=title, 
                        image=image, 
                        description=description, 
                        plot = plot,
                        medium=medium)

            new_results = Entity.objects.filter(title__icontains=user_input)[:12]
            return render(request, 'content/search_results.html', {'results': new_results})
        
        # return original list from database if results more than 10
        else:
            return render(request, 'content/search_results.html', {'results': results})
    else:
        return redirect('homepage')

def view_entity(request, entity_id):
    entity = get_object_or_404(Entity, id=entity_id)

    update_entity(entity.id) # update entity information before displaying

    context = {
        'entity': entity,
        # ... other context data ...
    }

    return render(request, 'content/entity_detail.html', context)

def update_entity(entity_id):
    entity = get_object_or_404(Entity, id=entity_id)

    entity.reviewed = Review.objects.filter(entity=entity).count() # update number of reviews
    sum_scores = Review.objects.filter(entity=entity).aggregate(models.Sum('final_score')).get('final_score__sum')
    if sum_scores is not None:
        entity.overall_score = sum_scores / entity.reviewed # update overall score
    entity.save()

    # Update EntityTag Counts
    entity_tags = EntityTag.objects.filter(entity=entity)
    for entity_tag in entity_tags:
        tag = entity_tag.tag
        count = Review.objects.filter(entity=entity, tags=tag).count()
        entity_tag.count = count
        entity_tag.save()