from datetime import timezone
from django.db import models
from users.models import User
from content.models import Entity, Tag
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from .signals import review_saved

# Create your models here.
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="reviews")
    entity = models.ForeignKey(Entity, on_delete=models.DO_NOTHING, related_name='reviews')
    tags = models.ManyToManyField(Tag, blank=True, limit_choices_to={'id__lte': 5}, related_name='reviews')
    category_rating1 = models.IntegerField(default=0, blank=True, null=True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    category_rating2 = models.IntegerField(default=0, blank=True, null=True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    category_rating3 = models.IntegerField(default=0, blank=True, null=True, validators=[MinValueValidator(-1), MaxValueValidator(1)])
    final_score = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=0.0,
        blank=True, null=True,
    )
    blurb = models.CharField(max_length=255, null=True)
    private = models.BooleanField(default=False, blank=True, null=True,)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.entity} review by {self.user}'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        review_saved.send(sender=self.__class__, instance=self)