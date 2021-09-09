from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.fields import CharField

PERMISSION_LEVEL_CHOICES = [
    ('admin', 'Администратор'),
    ('moderator', 'Модератор'),
    ('user', 'Пользователь')
]

class Profile(AbstractUser):
    bio = models.TextField('Биография',
                           blank=True)
    role = models.CharField(max_length=10,
                            choices=PERMISSION_LEVEL_CHOICES,
                            default='user')
    confirmation_code = models.CharField(max_length=100)