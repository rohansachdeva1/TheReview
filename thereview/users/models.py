from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.CharField(max_length=255)
    pic = models.ImageField(null=True, blank=True, upload_to="images/")

    def __str__(self):
        return str(self.user)