from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.urls import reverse
from content.models import Entity
from playlists.models import Playlist

# Create your views here.
def view_playlist(request, playlist_id):
    pass

def add_to_playlist(request, entity_id):
    entity = get_object_or_404(Entity, id=entity_id)

    # check if user has playlist for this medium
    try:
        playlist = Playlist.objects.get(user=request.user, medium=entity.medium)    
    except Playlist.DoesNotExist:
        playlist = Playlist.objects.create(user=request.user, medium=entity.medium)
    
    playlist.entities.add(entity)

    view_profile_url = reverse('view_profile', args=[request.user.username])
    return redirect(view_profile_url)

def delete_from_playlist(request, entity_id):
    pass
