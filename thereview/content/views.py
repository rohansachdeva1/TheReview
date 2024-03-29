import asyncio
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
import requests
from content.models import Medium, Entity, EntityTag, Genre, Actor, EntityActor, EntityLocation, StreamingService, Director
from users.models import User, UserTag, SearchHistory
from reviews.models import Review
from playlists.models import Playlist
from django.db import models
from .tasks import fetch_actor_info
import random
from django.db.models import Avg

# Main search function, can search entities and users right now
# future plans to divide into many functions instead of one big one
def search_entities(request):
    if request.method == "POST":
        request.session['search_page_url'] = request.get_full_path()
        user_input = request.POST['searched']
        
        results = Entity.objects.filter(title__icontains=user_input)[:12] # Query entities whose title contains the input
        users = User.objects.filter(username__icontains=user_input) # Query users whose username contains the input

        # use api if not enough objects in database
        if results.count() < 2:
            get_imdb_api(user_input)
            results = Entity.objects.filter(title__icontains=user_input)[:12]
        
        context = {
        'results': results,
        'users': users,
        }

        return render(request, 'content/search_tile_results.html', context)
        
    else:
        return redirect('homepage')

# Get actor information for a singular entity, entity id parameter
def get_imdb_api(user_input):

    data = requests.get('https://imdb-api.com/API/AdvancedSearch/k_28nyce3o?title=' + user_input).json()

    # loop through json object and create variables for needed fields
    if data is not None and 'results' in data:
        for item in data['results']:
            # only allow entities with imDbRatingVotes above 30k
            if item['imDbRatingVotes'] is not None and int(item['imDbRatingVotes']) > 30000:
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
                    imdbRating = item['imDbRating']
                    medium = Medium.objects.get(name='Movies')  # Default medium value for cases without resultType
                    
                    entity = Entity.objects.createentity_obj = Entity.objects.create(
                        api_id=id, 
                        slug_field=slug, 
                        title=title, 
                        image=image, 
                        year=year, 
                        plot = plot,
                        content_rating = content_rating,
                        imdbRating = imdbRating,
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
                    get_actor_info(entity.api_id)
    else:
        print("No Results Found")

# Get actor information for a singular entity, entity id parameter
def get_actor_info(entity_id):
    
    data = requests.get('https://imdb-api.com/en/API/FullCast/k_28nyce3o/' + entity_id).json()
    entity = Entity.objects.get(api_id=entity_id)

    # Loop through json object and create variables for needed fields
    if data['actors'] is not None:
        for item in data['actors'][:18]:
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
    
    directors = data.get('directors', {})
    if directors['items']:
        for item in directors['items']:
            api_id = item['id']
            name = item['name']

            # Create director obj if not already in database
            try:
                director = Director.objects.get(api_id=api_id)
            except Director.DoesNotExist:
                director = Director.objects.create(api_id=api_id, name=name)
            
            entity.directors.add(director)

def update_database(request, data):
    pass

# View entity information (basic info, tags, actors, reviews, locations, etc.) in the entity detail page
def view_entity(request, entity_id):
    entity = get_object_or_404(Entity, id=entity_id)
    entity_tags = EntityTag.objects.filter(entity=entity).order_by('-count')[:5]
    print(entity_tags)
    entity_actors = EntityActor.objects.filter(entity=entity)[:18]
    genre_recs = generate_genre_recs(entity_id)[:12]
    user = get_object_or_404(User, id=request.user.id)
    reviews = Review.objects.filter(entity=entity)
    locations = EntityLocation.objects.filter(entity=entity)
    full_stars = int(entity.overall_score)
    half_star_value = entity.overall_score - full_stars
    playlist_count = Playlist.objects.filter(entities__id=entity_id).count()
    try:
        watchlater = Playlist.objects.get(user=user, medium=entity.medium, auto_generated=True)
    except Playlist.DoesNotExist:
        watchlater = None
    user_playlists = Playlist.objects.filter(user=user, medium=entity.medium)
    is_reviewed = reviews.filter(user=request.user).exists()
    in_playlist = Playlist.objects.filter(user=request.user, entities=entity).exists()
    is_seen = entity in request.user.profile.seen.all()
    # seen_count = entity.profile_set.count()  

    update_entity(entity.id) # update entity information before displaying
    
    if entity.clicked is None:
        entity.clicked = 1
    else:
        entity.clicked += 1 # increment clicked for data collection
    entity.save()
    if request.user.is_authenticated:
        SearchHistory.objects.create(entity=entity, user=request.user)
    
    get_streaming(entity)

    context = {
        'entity': entity,
        'entity_tags': entity_tags,
        'entity_actors': entity_actors,
        'genre_recs': genre_recs,
        'watchlater': watchlater,
        'reviews': reviews,
        'locations': locations,
        'playlist_count': playlist_count,
        'user_playlists': user_playlists,
        'full_stars': full_stars,
        'half_star_value': half_star_value,
        'is_reviewed': is_reviewed,
        'in_playlist': in_playlist,
        'is_seen': is_seen,
    }

    return render(request, 'content/entity_detail.html', context)

# Get streaming information for a singular entity and establish connections between entity and streaming service
# NOT YET IMPLEMENTED: severing connection when entity is removed from streaming site
def get_streaming(entity):
    # testing for streaming availability api
    api_url = 'https://streaming-availability.p.rapidapi.com/v2/get/basic'
    api_key = 'ccf83e711emsh0d4ac5f679caffcp14f0e9jsne8d73428fe45'

    headers = {
        'X-RapidAPI-Key': api_key,
        'X-RapidAPI-Host': 'streaming-availability.p.rapidapi.com'
    }

    params = {
        'country': 'us',
        'imdb_id': entity.api_id,
        'output_language': 'en'
    }

    # Make the API call
    response = requests.get(api_url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()  # Store the JSON response in 'data' variable
    else:
        data = {'error': 'Failed to fetch streaming data.'} # Handle the API error here

    # find the available streaming services
    results = data.get('result', {}) # Access the 'results' dictionary
    streaming_info = results.get('streamingInfo', {}) # Access the 'streamingInfo' dictionary within 'results'
    us_info = streaming_info.get('us', {}) # Access the 'us' dictionary within 'streamingInfo'

    # Check if 'netflix', 'apple', 'prime', 'hulu', 'hbo', 'disney' have entity
    if 'netflix' in us_info:
        #streaming_services['Netflix'] = us_info['netflix'][0]['link']
        loc = StreamingService.objects.get(name='Netflix')
        if (not EntityLocation.objects.filter(entity=entity, location=loc)):
            link = us_info['netflix'][0]['link']
            EntityLocation.objects.create(entity=entity, location=loc, link=link)

    if 'disney' in us_info:
        loc = StreamingService.objects.get(name='Disney')
        if (not EntityLocation.objects.filter(entity=entity, location=loc)):
            link = us_info['disney'][0]['link']
            EntityLocation.objects.create(entity=entity, location=loc, link=link)

    if 'apple' in us_info:
        loc = StreamingService.objects.get(name='Apple')
        if (not EntityLocation.objects.filter(entity=entity, location=loc)):
            link = us_info['apple'][0]['link']
            EntityLocation.objects.create(entity=entity, location=loc, link=link)

    if 'prime' in us_info:
        loc = StreamingService.objects.get(name='Prime')
        if (not EntityLocation.objects.filter(entity=entity, location=loc)):
            link = us_info['prime'][0]['link']
            EntityLocation.objects.create(entity=entity, location=loc, link=link)

    if 'hulu' in us_info:
        loc = StreamingService.objects.get(name='Hulu')
        if (not EntityLocation.objects.filter(entity=entity, location=loc)):
            link = us_info['hulu'][0]['link']
            EntityLocation.objects.create(entity=entity, location=loc, link=link)
            
    if 'hbo' in us_info:
        loc = StreamingService.objects.get(name='HBO')
        if (not EntityLocation.objects.filter(entity=entity, location=loc)):
            link = us_info['hbo'][0]['link']
            EntityLocation.objects.create(entity=entity, location=loc, link=link)

    # Print the names and links of the streaming services
    # for service, link in streaming_services.items():
    #     print(f"{service}: {link}")

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

def generate_genre_recs(entity_id):
    entity = get_object_or_404(Entity, id=entity_id)
    genres = entity.genres.all()  # get all genres associated with that entity
    
    related_entities = Entity.objects.filter(genres__in=genres).exclude(id=entity_id)
    for genre in genres:
        related_entities = related_entities.filter(genres=genre)
    related_entities = related_entities.distinct()
    #random_entities = random.sample(list(related_entities), min(12, len(related_entities)))

    return related_entities

def generate_tag_recs(user_id):
    user = get_object_or_404(User, id=user_id)
    user_tags = UserTag.objects.filter(user=user).annotate(average_score=Avg('sum_scores')).filter(average_score__gt=4)
    # get the tags
    # find other movies with those tags as the top 3
        