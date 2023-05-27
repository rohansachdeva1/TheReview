from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Medium(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Genre(models.Model):
    name = models.CharField(max_length=255)
    medium = models.ForeignKey(Medium, on_delete=models.CASCADE)
    entity = models.ManyToManyField('Entity', related_name='GenreEntityLinker', blank=True)

    def __str__(self):
        return self.name
    
class Entity(models.Model):
    api_id = models.CharField(max_length=500, null=True, blank=True)
    slug_field = models.CharField(max_length=500, null=True, blank=True)
    image = models.CharField(max_length=500, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500, null=True, blank=True)
    overall_score = models.IntegerField(null=True, blank=True)
    overall_rating1 = models.FloatField(null=True, blank=True)
    overall_rating2 = models.FloatField(null=True, blank=True)
    overall_rating3 = models.FloatField(null=True, blank=True)
    overall_rating4 = models.FloatField(null=True, blank=True)
    overall_rating5 = models.FloatField(null=True, blank=True)
    genre = models.ManyToManyField(Genre, related_name='GenreEntityLinker')
    medium = models.ForeignKey(Medium, on_delete=models.CASCADE)

    # metrics
    clean = models.BooleanField(null=True, blank=True) # if entity is considered clean or unsure (our definition)
    searched = models.IntegerField(null=True, blank=True) # number of times appeared in search
    clicked = models.IntegerField(null=True, blank=True) # number of times user clicked into detail page
    added_to_playlist = models.IntegerField(null=True, blank=True) # number of times user added to playlist
    reviewed = models.IntegerField(null=True, blank=True) # number of times user reviewed

    def __str__(self):
        return self.title
    
class Category(models.Model):
    name = models.CharField(max_length=255)
    medium = models.ForeignKey(Medium, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Actor(models.Model):
    api_id = models.CharField(max_length=500, null=True, blank=True)
    name = models.CharField(max_length=255)
    image = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name
    
class EntityActor(models.Model):
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    as_character = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name