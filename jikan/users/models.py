from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

class CustomUserManager(UserManager):
    pass

class CustomUser(AbstractUser):
    objects = CustomUserManager()

class UserProfile(models.Model):
    user = models.ForeignKey(CustomUser, unique=True, on_delete=models.CASCADE)
    institute = models.CharField(max_length=50, blank=True)
    url = models.URLField("Website", blank=True)

CustomUser.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
