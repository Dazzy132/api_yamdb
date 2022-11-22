from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ROLES = (
        ('user', 'Аутентифицированный пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор'),
    )

    email = models.EmailField('email address', unique=True)
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        'Пользовательская роль',
        choices=ROLES,
        default='user',
        max_length=30,
    )

    class Meta:
        ordering = ('pk',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
