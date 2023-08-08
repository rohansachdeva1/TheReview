from django.db import models
from users.models import User
from content.models import Medium, Entity

# Create your models here.
class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists')
    medium = models.ForeignKey(Medium, on_delete=models.CASCADE, related_name='playlists')
    entities = models.ManyToManyField(Entity, related_name='playlists')
    name = models.CharField(max_length=30, null=True)
    auto_generated = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return f'{self.user}\'s {self.name} playlist'