from django.contrib.auth.models import AbstractUser
from django.db import models
from .validators import validate_username
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):

    ROLES = (
        ('user', 'Аутентифицированный пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор'),
    )

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        validators=[validate_username],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
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
