from django.db import models

# Create your models here.
class Medium(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Genre(models.Model):
    name = models.CharField(max_length=255)
    mediums = models.ForeignKey(Medium, on_delete=models.CASCADE)
    entities = models.ManyToManyField('Entity', related_name='GenreEntityLinker')

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
    genres = models.ManyToManyField(Genre, related_name='GenreEntityLinker')
    mediums = models.ForeignKey(Medium, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class Category(models.Model):
    name = models.CharField(max_length=255)
    mediums = models.ForeignKey(Medium, on_delete=models.CASCADE)

    def __str__(self):
        return self.name