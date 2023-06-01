from datetime import timezone
from django.db import models
from users.models import User
from content.models import Entity, Tag
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name='reviews')
    tags = models.ManyToManyField(Tag, related_name='reviews')
    category_rating1 = models.IntegerField(default=0, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    category_rating2 = models.IntegerField(default=0, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    category_rating3 = models.IntegerField(default=0, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    category_rating4 = models.IntegerField(default=0, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    final_score = models.FloatField(null=True, blank=True)
    blurb = models.CharField(max_length=255)
    private = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.entity} review by {self.user}'