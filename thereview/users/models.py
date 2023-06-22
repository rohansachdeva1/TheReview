from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from content.models import Tag, Entity
from decimal import Decimal

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.CharField(max_length=255)
    profile_image = models.ImageField(null=True, blank=True, upload_to="profile/")
    email = models.EmailField(null=True, blank=True)
    reviewed = models.IntegerField(default=0, null=True, blank=True)
    avg_rating = models.DecimalField(default=Decimal('0.0'), max_digits=3, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return str(self.user)
    
def create_profile(sender, instance, created, **kwargs):
            if created:
                user_profile = Profile(user=instance)
                # add defaults (profile pic, bio)
                user_profile.save()

post_save.connect(create_profile, sender=User)

class UserTag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    sum_scores = models.FloatField(default=0)
    count = models.IntegerField(default=1, null=True, blank=True)

    def __str__(self):
        return f'{self.user} - {self.tag}'
    
class UserEntity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)
    value = models.FloatField(default=0)

    def __str__(self):
        return f'{self.user} - {self.entity}'