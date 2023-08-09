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
    #playlist = get_object_or_404(Playlist, id=playlist_id)

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

def add_to_new_playlist(request, entity_id, playlist_id):
    entity = get_object_or_404(Entity, id=entity_id)
    playlist = get_object_or_404(Playlist, id=playlist_id)
    
    if request.method == 'POST': # once user has filled our form
        name = request.POST['name'] # get username and password from request object
        playlist = Playlist.objects.create(user=request.user, medium=entity.medium, name=name)
        playlist.entities.add(entity)
        messages.success(request, entity.title + " Added to " + playlist.name + " Successfully!")
    else:
        return render(request, 'users/login.html') # REPLACE WITH CREATE PLAYLIST TEMPLATE
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def delete_from_playlist(request, entity_id, playlist_id):
    entity = get_object_or_404(Entity, id=entity_id)
    # user = get_object_or_404(User, id=request.user.id)
    playlist = get_object_or_404(Playlist, id=playlist_id)
    #playlist = get_object_or_404(Playlist, user=user, medium=entity.medium)
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

    messages.success(request, entity.title + " Added to " + watchlater.name + " Successfully!")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def delete_from_watchlater(request, entity_id):
    entity = get_object_or_404(Entity, id=entity_id)
    user = get_object_or_404(User, id=request.user.id)
    watchlater = get_object_or_404(Playlist, user=user, medium=entity.medium, auto_generated=True)
    #playlist_entities = playlist.entities.all()

    watchlater.entities.remove(entity)

    messages.success(request, entity.title + " Removed From " + watchlater.name + " Successfully!")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    


    
