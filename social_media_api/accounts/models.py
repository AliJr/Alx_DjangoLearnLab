from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# Custom user model extending AbstractUser
class CustomUser(AbstractUser):
    bio = models.TextField(max_length=200, null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", null=True, blank=True
    )
    followers = models.ManyToManyField("self", symmetrical=False, blank=True)
