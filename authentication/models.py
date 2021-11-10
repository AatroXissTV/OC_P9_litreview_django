from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    profile_photo = models.ImageField()

    follows = models.ManyToManyField(
        'self',
        symmetrical=False,
        verbose_name='follows',
    )
