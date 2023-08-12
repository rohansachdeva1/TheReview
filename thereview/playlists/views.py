from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.urls import reverse
from content.models import Entity
from playlists.models import Playlist
from django.contrib import messages

# View all entities in existing playlist
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

# Add to existing playlist by user selection, entity id parameter, playlist id from POST request form
def add_to_playlist(request, entity_id):
    entity = get_object_or_404(Entity, id=entity_id)

    if request.method == "POST":
            playlist_id = request.POST.get("playlist")
            new_playlist_name = request.POST.get("new_playlist_name")
            
            if playlist_id == "new":
                playlist = Playlist.objects.create(name=new_playlist_name, medium=entity.medium, user=request.user)
            else:
                playlist = Playlist.objects.get(id=playlist_id, user=request.user)
            
            playlist.entities.add(entity)
            messages.success(request, entity.title + " Added to " + playlist.name + " Successfully!")
            #return redirect("playlist_list")  # Redirect to a page that lists the playlists
        
    # Handle GET request or any other cases if needed
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

# create new playlist and add entity to it, entity id parameter
def add_to_new_playlist(request, entity_id):
    entity = get_object_or_404(Entity, id=entity_id)

    if request.method == "POST":
        new_playlist_name = request.POST.get("new_playlist_name")
        
        playlist = Playlist.objects.create(name=new_playlist_name, medium=entity.medium, user=request.user)
        
        playlist.entities.add(entity)
        messages.success(request, entity.title + " Added to " + playlist.name + " Successfully!")
        
    # Handle GET request or any other cases if needed
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

# Delete from existing playlist, entity id and playlist id parameter
def delete_from_playlist(request, entity_id, playlist_id):
    entity = get_object_or_404(Entity, id=entity_id)
    playlist = get_object_or_404(Playlist, id=playlist_id)

    playlist.entities.remove(entity)

    messages.success(request, "Entity Removed From Playlist Successfully!")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

# Add to watch later auto generated playlist, entity id parameter, implemented in entity detail page
def add_to_watchlater(request, entity_id):
    entity = get_object_or_404(Entity, id=entity_id)
    name = entity.medium.name + " For Later"

    # check if user has playlist for this medium
    try:
        watchlater = Playlist.objects.get(user=request.user, medium=entity.medium, auto_generated=True)    
    except Playlist.DoesNotExist:
        watchlater = Playlist.objects.create(user=request.user, medium=entity.medium, auto_generated=True, name=name)
    
    watchlater.entities.add(entity)

    messages.success(request, entity.title + " Added to " + watchlater.name + " Successfully!")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

# Delete from watch later auto generated playlist, entity id parameter, implemented in entity detail page
def delete_from_watchlater(request, entity_id):
    entity = get_object_or_404(Entity, id=entity_id)
    user = get_object_or_404(User, id=request.user.id)
    watchlater = get_object_or_404(Playlist, user=user, medium=entity.medium, auto_generated=True)
    #playlist_entities = playlist.entities.all()

    watchlater.entities.remove(entity)

    messages.success(request, entity.title + " Removed From " + watchlater.name + " Successfully!")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

# Delete a review from profile
def delete_playlist(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id)
    playlist.delete()

    # view_profile_url = reverse('view_profile', args=[review.user.username])
    # return redirect(view_profile_url)
    return redirect('view_profile', playlist.user.username)


    
