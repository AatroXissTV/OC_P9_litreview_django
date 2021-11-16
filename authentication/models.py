# django imports
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """ Represent a User.
    - Uses the Abstract User of Django
    - Added a field for a profile picture"""
    profile_photo = models.ImageField()
