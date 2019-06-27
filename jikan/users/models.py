from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

class CustomUserManager(UserManager):
    pass

class CustomUser(AbstractUser):
    objects = CustomUserManager()
    institution = models.CharField(max_length=50, blank=True)
    url = models.URLField("Website", blank=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)

    REQUIRED_FIELDS = ['first_name', 'last_name']

CustomUser.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
