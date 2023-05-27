from django.db import models
from users.models import User
from content.models import Entity

# Create your models here.
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="reviews")
    entity = models.ForeignKey(Entity, on_delete=models.DO_NOTHING, related_name='reviews')
    rating1 = models.BinaryField()
    rating2 = models.BinaryField()
    rating3 = models.BinaryField()
    rating4 = models.BinaryField()
    rating5 = models.BinaryField()
    final_score = models.FloatField()
    blurb = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.entity} review by {self.user}'