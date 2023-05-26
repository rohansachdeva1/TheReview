from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.CharField(max_length=255)
    profile_image = models.ImageField(null=True, blank=True, upload_to="profile/")

    def __str__(self):
        return str(self.user)
    
def create_profile(sender, instance, created, **kwargs):
        if created:
            user_profile = Profile(user=instance)
            # add defaults (profile pic, bio)
            user_profile.save()

post_save.connect(create_profile, sender=User)