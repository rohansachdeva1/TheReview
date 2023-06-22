from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from decimal import Decimal

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
    description = models.CharField(max_length=100, null=True, blank=True)
    plot = models.CharField(max_length=500, null=True, blank=True)
    overall_score = models.DecimalField(
        default=0.0,
        null=True,
        blank=True,
        max_digits=5,
        decimal_places=2
    )
    genre = models.ManyToManyField(Genre, related_name='GenreEntityLinker')
    medium = models.ForeignKey(Medium, on_delete=models.DO_NOTHING)
    tag = models.ManyToManyField('Tag', through='EntityTag')

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
    order = models.IntegerField(null=True)
    medium = models.ForeignKey(Medium, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Tag(models.Model):
    medium = models.ForeignKey(Medium, on_delete=models.CASCADE)
    icon = models.ImageField(null=True, blank=True, upload_to="icons/")
    name = models.CharField(max_length=100)
    base_emotion = models.ForeignKey('BaseEmotion', null=True, blank=True, on_delete=models.DO_NOTHING)
    derived_emotion = models.ForeignKey('DerivedEmotion', null=True, blank=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name
    
class BaseEmotion(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class DerivedEmotion(models.Model):
    base_emotion = models.ForeignKey(BaseEmotion, null=True, blank=True, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class EntityTag(models.Model):
    entity = models.ForeignKey(Entity, on_delete=models.DO_NOTHING)
    tag = models.ForeignKey(Tag, on_delete=models.DO_NOTHING)
    count = models.IntegerField(default=1, null=True, blank=True)

    def __str__(self):
        return f'{self.entity} - {self.tag}'


class Actor(models.Model):
    api_id = models.CharField(max_length=500, null=True, blank=True)
    name = models.CharField(max_length=255)
    image = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name
    
class EntityActor(models.Model):
    entity = models.ForeignKey(Entity, on_delete=models.DO_NOTHING)
    actor = models.ForeignKey(Actor, on_delete=models.DO_NOTHING)
    as_character = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f'{self.actor} in {self.entity}'