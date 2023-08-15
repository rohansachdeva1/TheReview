from django.db import models
from users.models import User
from content.models import Medium, Entity

# Create your models here.
class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists')
    medium = models.ForeignKey(Medium, on_delete=models.CASCADE, related_name='playlists')
    entities = models.ManyToManyField(Entity, related_name='playlists')
    name = models.CharField(max_length=30, null=True)
    description = models.CharField(max_length=500, null=True)
    auto_generated = models.BooleanField(default=False, blank=True, null=True)
    likes = models.ManyToManyField(User, related_name="playlist_likes", blank=True)

    # Keep track of the amount of likes
    def number_of_likes(self):
        return self.likes.count()
    
    # Keep track of the amount of entities
    def number_of_entities(self):
        return self.entities.count()

    def __str__(self):
        return f'{self.user}\'s {self.name} playlist'