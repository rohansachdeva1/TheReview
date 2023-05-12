from django.db import models


class User(models.Model):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField()
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.username
    
class Medium(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Genre(models.Model):
    name = models.CharField(max_length=255)
    mediums = models.ManyToManyField(Medium, related_name='genres')
    entities = models.ManyToManyField('Entity', related_name='genres')

    def __str__(self):
        return self.name
    
class Entity(models.Model):
    image = models.BinaryField()
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    overall_score = models.IntegerField()
    overall_rating1 = models.FloatField()
    overall_rating2 = models.FloatField()
    overall_rating3 = models.FloatField()
    overall_rating4 = models.FloatField()
    overall_rating5 = models.FloatField()
    genres = models.ManyToManyField(Genre, related_name='entities')
    mediums = models.ManyToManyField(Medium, related_name='entities')

    def __str__(self):
        return self.title


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name='reviews')
    rating1 = models.FloatField()
    rating2 = models.FloatField()
    rating3 = models.FloatField()
    rating4 = models.FloatField()
    rating5 = models.FloatField()
    blurb = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.entity} review by {self.user}'


class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    medium = models.ForeignKey(Medium, on_delete=models.CASCADE)
    entities = models.ManyToManyField(Entity, related_name='playlists')

    def __str__(self):
        return f'{self.user}\'s {self.medium} playlist'


class Category(models.Model):
    name = models.CharField(max_length=255)
    mediums = models.ManyToManyField(Medium, related_name='categories')

    def __str__(self):
        return self.name


