from django.db import models
from users.models import User
from content.models import Entity

# Create your models here.
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