from django.db import models
from users.models import User
from content.models import Medium, Entity

# Create your models here.
class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    medium = models.ForeignKey(Medium, on_delete=models.CASCADE)
    entities = models.ManyToManyField(Entity, related_name='playlists')

    def __str__(self):
        return f'{self.user}\'s {self.medium} playlist'