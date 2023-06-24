import asyncio
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
import requests
from content.models import Medium, Entity, EntityTag, Genre, Actor, EntityActor
from reviews.models import Review
from django.db import models
from .tasks import fetch_actor_info

def search_entities(request):
    if request.method == "POST":
        request.session['search_page_url'] = request.get_full_path()
        user_input = request.POST['searched']
        
        results = Entity.objects.filter(title__icontains=user_input)[:12]

        # use api if not enough objects in database
        if results.count() < 5:
            data = requests.get('https://imdb-api.com/API/AdvancedSearch/k_28nyce3o?title=' + user_input).json()

            # loop through json object and create variables for needed fields
            for item in data['results']:
                # only allow entities with imDbRatingVotes above 10k
                if item['imDbRatingVotes'] is not None and int(item['imDbRatingVotes']) > 10000:
                    id = item['id']
                    
                    # prevent duplicates by checking if we already have an entity with that id, create new entity object and save
                    if (not Entity.objects.filter(api_id=id)):
                        
                        title = item['title']
                        slug = title.replace(' ', '-').lower()
                        image = item['image']
                        year = item['description']
                        plot = item['plot']
                        runtime = item['runtimeStr']
                        content_rating = item['contentRating']
                        medium = Medium.objects.get(name='Movies')  # Default medium value for cases without resultType
                        
                        entity = Entity.objects.createentity_obj = Entity.objects.create(
                            api_id=id, 
                            slug_field=slug, 
                            title=title, 
                            image=image, 
                            year=year, 
                            plot = plot,
                            content_rating = content_rating,
                            runtime = runtime,
                            medium=medium)
                        
                        # add genres to the entity
                        for genre in item['genreList']:
                            try:
                                curr_genre = Genre.objects.get(name=genre['key'])
                                
                            except Genre.DoesNotExist:
                                curr_genre = Genre(name=genre['key'], medium=medium)
                                curr_genre.save()
                                curr_genre.entities.add(entity)
                        
                            entity.genres.add(curr_genre)

                        # get actor info from full cast api, link them to entity using EntityActor model
                        fetch_actor_info(entity.api_id)
                            
            new_results = Entity.objects.filter(title__icontains=user_input)[:12]
            return render(request, 'content/search_tile_results.html', {'results': new_results})
        
        # return original list from database if results more than 10
        else:
            return render(request, 'content/search_tile_results.html', {'results': results})
    else:
        return redirect('homepage')
    
def fetch_actor_info(entity_id):
    
    data = requests.get('https://imdb-api.com/en/API/FullCast/k_28nyce3o/' + entity_id).json()
    entity = Entity.objects.get(api_id=entity_id)

    # Loop through json object and create variables for needed fields
    if data['actors'] is not None:
        for item in data['actors'][:5]:
            api_id = item['id']
            image = item['image']
            name = item['name']
            asCharacter = item['asCharacter']

            # Create actor obj if not already in database
            try:
                actor = Actor.objects.get(api_id=api_id)
            except Actor.DoesNotExist:
                actor = Actor.objects.create(api_id=api_id, name=name, image=image)

            # Link to entity using EntityActor model
            EntityActor.objects.create(entity=entity, actor=actor, as_character=asCharacter)

def view_entity(request, entity_id):
    entity = get_object_or_404(Entity, id=entity_id)
    entity_tags = EntityTag.objects.filter(entity=entity)
    entity_actors = EntityActor.objects.filter(entity=entity)

    update_entity(entity.id) # update entity information before displaying

    context = {
        'entity': entity,
        'entity_tags': entity_tags,
        'entity_actors': entity_actors,
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
        if entity_tag.count < 1:
            entity_tag.delete()
        