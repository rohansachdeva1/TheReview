from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.urls import reverse
from content.models import Entity
from playlists.models import Playlist
from django.contrib import messages

# Create your views here.
def view_playlist(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id)
    playlist_entities = playlist.entities.all()
    user = playlist.user

    # store data to be used in playlist_detail template in context
    context = {
        'playlist': playlist,
        'playlist_entities': playlist_entities,
        'user': user,
        # ... other context data ...
    }

    return render(request, 'playlists/playlist_detail.html', context)

def add_to_playlist(request, entity_id):
    entity = get_object_or_404(Entity, id=entity_id)

    # check if user has playlist for this medium
    try:
        playlist = Playlist.objects.get(user=request.user, medium=entity.medium)    
    except Playlist.DoesNotExist:
        playlist = Playlist.objects.create(user=request.user, medium=entity.medium)
    
    playlist.entities.add(entity)
    # if entity.added_to_playlist is None:
    #     entity.added_to_playlist = 1
    # else:
    #     entity.added_to_playlist += 1
    entity.save()

    messages.success(request, "Entity Added to Playlist Successfully!")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def delete_from_playlist(request, entity_id):
    entity = get_object_or_404(Entity, id=entity_id)
    user = get_object_or_404(User, id=request.user.id)
    playlist = get_object_or_404(Playlist, user=user, medium=entity.medium)
    #playlist_entities = playlist.entities.all()

    playlist.entities.remove(entity)

    # entity.added_to_playlist -= 1
    entity.save()

    messages.success(request, "Entity Removed From Playlist Successfully!")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def add_to_watchlater(request, entity_id):
    entity = get_object_or_404(Entity, id=entity_id)
    name = entity.medium.name + " For Later"

    # check if user has playlist for this medium
    try:
        watchlater = Playlist.objects.get(user=request.user, medium=entity.medium, auto_generated=True)    
    except Playlist.DoesNotExist:
        watchlater = Playlist.objects.create(user=request.user, medium=entity.medium, auto_generated=True, name=name)
    
    watchlater.entities.add(entity)

    messages.success(request, "Entity Added to Watch Later Successfully!")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def delete_from_watchlater(request, entity_id):
    entity = get_object_or_404(Entity, id=entity_id)
    user = get_object_or_404(User, id=request.user.id)
    playlist = get_object_or_404(Playlist, user=user, medium=entity.medium, auto_generated=True)
    #playlist_entities = playlist.entities.all()

    playlist.entities.remove(entity)

    # entity.added_to_playlist -= 1
    entity.save()

    messages.success(request, "Entity Removed From Playlist Successfully!")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    


    
