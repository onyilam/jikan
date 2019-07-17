from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

POSITION_OPTIONS =[("1", "Undergraduate Student"), ("2", "Graduate Student"),
("3", "Assistant Professor"),
("4", "Associate Professor"), ("5", "Professor"), ("6", "Non-academic Researcher")]

class CustomUserManager(UserManager):
    pass

class CustomUser(AbstractUser):
    objects = CustomUserManager()
    institution = models.CharField(max_length=50, blank=True)
    url = models.URLField("Website", blank=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    position = models.CharField(max_length=100, null=True, choices=POSITION_OPTIONS)
    research_area = models.TextField(null=True)

    REQUIRED_FIELDS = ['first_name', 'last_name']

CustomUser.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
