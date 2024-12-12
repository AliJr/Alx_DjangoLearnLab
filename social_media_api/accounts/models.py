from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager


# Custom user manager.
class UserManger(BaseUserManager):
    def create_user(self, username, password):
        if not username:
            raise ValueError("User must have a username")
        user = self.model(username=self.model.normalize_username(username))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):

        user = self.create_user(username, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


# Custom user model extending AbstractUser
class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", blank=True, null=True
    )
    follower = models.ManyToManyField(
        "self", related_name="followers", symmetrical=False, blank=True)
    following = models.ManyToManyField(
        "self", related_name="followings", symmetrical=False, blank=True
    )

    def __str__(self):
        return self.username

    def count_followers(self):
        return self.followers.count()

    def count_following(self):
        return self.following.count()
