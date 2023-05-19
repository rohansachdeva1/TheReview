from django.db import models

# Create your models here.
class Medium(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Genre(models.Model):
    name = models.CharField(max_length=255)
    medium = models.ForeignKey(Medium, on_delete=models.CASCADE)
    entity = models.ManyToManyField('Entity', related_name='GenreEntityLinker')

    def __str__(self):
        return self.name
    
class Entity(models.Model):
    image = models.BinaryField(null=True)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True)
    overall_score = models.IntegerField(null=True)
    overall_rating1 = models.FloatField(null=True)
    overall_rating2 = models.FloatField(null=True)
    overall_rating3 = models.FloatField(null=True)
    overall_rating4 = models.FloatField(null=True)
    overall_rating5 = models.FloatField(null=True)
    genre = models.ManyToManyField(Genre, related_name='GenreEntityLinker')
    medium = models.ForeignKey(Medium, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class Category(models.Model):
    name = models.CharField(max_length=255)
    medium = models.ForeignKey(Medium, on_delete=models.CASCADE)

    def __str__(self):
        return self.name